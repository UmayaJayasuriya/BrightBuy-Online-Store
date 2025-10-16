from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.variant import Variant
from app.models.product import Product
from app.schemas.cart import CartOut, AddToCartRequest, CartItemOut
from typing import List
from datetime import datetime
from app.models.order import Order, OrderItem, Payment
from pydantic import BaseModel
from typing import Optional

# Checkout request schema
class CheckoutRequest(BaseModel):
    user_id: int
    cart_id: int
    payment_method: Optional[str] = "cash"

router = APIRouter(prefix="/cart", tags=["cart"])


def get_current_user_id(user_id: int):
    """
    Dependency to get current user ID from authentication
    For now, we'll pass it as a parameter, but this should be replaced with actual JWT auth
    """
    return user_id


@router.post("/add", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    request: AddToCartRequest,
    user_id: int,  # This should come from JWT token in production
    db: Session = Depends(get_db)
):
    """
    Add a variant to the user's cart
    Creates a new cart if user doesn't have one
    """
    try:
        # Get variant details
        variant = db.query(Variant).filter(Variant.variant_id == request.variant_id).first()
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")

        # Check if variant has a price
        if variant.price is None:
            raise HTTPException(status_code=400, detail="Variant price not available")

        # Get or create cart for user
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id, total_amount=0.0)
            db.add(cart)
            db.commit()
            db.refresh(cart)

        # Check if variant already in cart
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.cart_id,
            CartItem.variant_id == request.variant_id
        ).first()

        if existing_item:
            # Update quantity
            existing_item.quantity += request.quantity
            db.commit()
            db.refresh(existing_item)
            cart_item = existing_item
        else:
            # Create new cart item (no price column in cart_item table)
            cart_item = CartItem(
                cart_id=cart.cart_id,
                variant_id=request.variant_id,
                quantity=request.quantity
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)

        # Update cart total_amount
        total = 0.0
        all_items = db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).all()
        for item in all_items:
            item_variant = db.query(Variant).filter(Variant.variant_id == item.variant_id).first()
            if item_variant and item_variant.price:
                total += float(item_variant.price) * item.quantity
        
        cart.total_amount = total
        db.commit()

        # Get product name for response
        product = db.query(Product).filter(Product.product_id == variant.product_id).first()
        
        # Prepare response
        response = CartItemOut(
            cart_item_id=cart_item.cart_item_id,
            cart_id=cart_item.cart_id,
            variant_id=cart_item.variant_id,
            quantity=cart_item.quantity,
            price=float(variant.price),  # Get price from variant, not cart_item
            variant_name=variant.variant_name,
            product_name=product.product_name if product else None,
            product_id=variant.product_id
        )

        return response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add to cart: {str(e)}")


@router.get("/{user_id}", response_model=CartOut)
def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Get user's cart with all items
    """
    try:
        # Get cart with items
        cart = db.query(Cart).options(
            joinedload(Cart.cart_items).joinedload(CartItem.variant)
        ).filter(Cart.user_id == user_id).first()

        if not cart:
            # Return empty cart
            return CartOut(
                cart_id=0,
                user_id=user_id,
                created_date=None,
                total_amount=0.0,
                cart_items=[]
            )

        # Build cart items with product details
        cart_items_out = []
        total = 0.0

        for item in cart.cart_items:
            variant = item.variant
            product = db.query(Product).filter(Product.product_id == variant.product_id).first()
            
            # Get price from variant since cart_item doesn't have price column
            item_price = float(variant.price) if variant.price else 0.0
            item_total = item_price * item.quantity
            total += item_total

            cart_items_out.append(CartItemOut(
                cart_item_id=item.cart_item_id,
                cart_id=item.cart_id,
                variant_id=item.variant_id,
                quantity=item.quantity,
                price=item_price,
                variant_name=variant.variant_name,
                product_name=product.product_name if product else None,
                product_id=variant.product_id
            ))

        # Update cart total_amount if different
        if cart.total_amount != total:
            cart.total_amount = total
            db.commit()

        return CartOut(
            cart_id=cart.cart_id,
            user_id=cart.user_id,
            created_date=cart.created_date,
            total_amount=float(cart.total_amount) if cart.total_amount else 0.0,
            cart_items=cart_items_out
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cart: {str(e)}")


@router.put("/update/{cart_item_id}")
def update_cart_item_quantity(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """
    Update quantity of a cart item
    """
    try:
        cart_item = db.query(CartItem).filter(CartItem.cart_item_id == cart_item_id).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")

        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            db.delete(cart_item)
        else:
            cart_item.quantity = quantity

        db.commit()
        
        # Update cart total_amount
        cart = db.query(Cart).filter(Cart.cart_id == cart_item.cart_id).first()
        if cart:
            total = 0.0
            all_items = db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).all()
            for item in all_items:
                variant = db.query(Variant).filter(Variant.variant_id == item.variant_id).first()
                if variant and variant.price:
                    total += float(variant.price) * item.quantity
            cart.total_amount = total
            db.commit()
        
        return {"message": "Cart item updated successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update cart item: {str(e)}")


@router.delete("/remove/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db)):
    """
    Remove an item from cart
    """
    try:
        cart_item = db.query(CartItem).filter(CartItem.cart_item_id == cart_item_id).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")

        cart_id = cart_item.cart_id
        db.delete(cart_item)
        db.commit()
        
        # Update cart total_amount
        cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
        if cart:
            total = 0.0
            all_items = db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).all()
            for item in all_items:
                variant = db.query(Variant).filter(Variant.variant_id == item.variant_id).first()
                if variant and variant.price:
                    total += float(variant.price) * item.quantity
            cart.total_amount = total
            db.commit()
        
        return {"message": "Item removed from cart successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to remove item: {str(e)}")


@router.delete("/clear/{user_id}")
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Clear all items from user's cart
    """
    try:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        # Delete all cart items
        db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
        db.commit()

        return {"message": "Cart cleared successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear cart: {str(e)}")


# Checkout endpoint
@router.post("/checkout")
def checkout_cart(request: CheckoutRequest, db: Session = Depends(get_db)):
    """Checkout: create order, order_items, payment, clear cart"""
    try:
        # Get cart and items
        cart = db.query(Cart).filter(Cart.cart_id == request.cart_id, Cart.user_id == request.user_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Create order
        order = Order(
            cart_id=cart.cart_id,
            user_id=cart.user_id,
            order_date=datetime.utcnow(),
            total_amount=cart.total_amount or 0.0
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Create order items
        for item in cart_items:
            variant = db.query(Variant).filter(Variant.variant_id == item.variant_id).first()
            price = float(variant.price) if variant and variant.price else 0.0
            order_item = OrderItem(
                order_id=order.order_id,
                quantity=item.quantity,
                price=price
            )
            db.add(order_item)

        db.commit()

        # Create payment record
        payment = Payment(
            order_id=order.order_id,
            payment_method=request.payment_method or "cash",
            payment_status="pending",
            payment_date=datetime.utcnow()
        )
        db.add(payment)
        db.commit()

        # Clear cart
        for item in cart_items:
            db.delete(item)
        cart.total_amount = 0.0
        db.commit()

        return {"order_id": order.order_id, "message": "Order placed successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Checkout failed: {str(e)}")
