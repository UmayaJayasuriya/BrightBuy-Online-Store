"""
Cart Routes - Converted to MySQL Connector
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from app.database import get_db
from app.schemas.cart import CartOut, AddToCartRequest, CartItemOut
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/cart", tags=["cart"])


class AddItemRequest(BaseModel):
    variant_id: int
    quantity: int = 1


@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    user_id: int = Query(..., description="User ID"),
    item: AddItemRequest = Body(...),
    db=Depends(get_db)
):
    """Add product variant to cart"""
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Check if cart exists for user
        cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        
        if not cart:
            # Create new cart
            cursor.execute("INSERT INTO cart (user_id, total_amount) VALUES (%s, 0)", (user_id,))
            db.commit()
            cart_id = cursor.lastrowid
        else:
            cart_id = cart['cart_id']
        
        # Check if item already in cart
        cursor.execute(
            "SELECT * FROM cart_item WHERE cart_id = %s AND variant_id = %s",
            (cart_id, item.variant_id)
        )
        existing_item = cursor.fetchone()
        
        if existing_item:
            # Update quantity
            new_qty = existing_item['quantity'] + item.quantity
            cursor.execute(
                "UPDATE cart_item SET quantity = %s WHERE cart_item_id = %s",
                (new_qty, existing_item['cart_item_id'])
            )
        else:
            # Add new item
            cursor.execute(
                "INSERT INTO cart_item (cart_id, variant_id, quantity) VALUES (%s, %s, %s)",
                (cart_id, item.variant_id, item.quantity)
            )
        
        # Recalculate cart total
        cursor.execute("""
            SELECT SUM(ci.quantity * v.price) as total
            FROM cart_item ci
            JOIN variant v ON ci.variant_id = v.variant_id
            WHERE ci.cart_id = %s
        """, (cart_id,))
        total_result = cursor.fetchone()
        new_total = float(total_result['total']) if total_result and total_result['total'] else 0.0
        
        # Update cart total_amount
        cursor.execute(
            "UPDATE cart SET total_amount = %s WHERE cart_id = %s",
            (new_total, cart_id)
        )
        
        db.commit()
        cursor.close()
        
        return {"message": "Item added to cart successfully", "cart_id": cart_id, "new_total": new_total}
        
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error adding to cart: {str(e)}")


@router.get("/{user_id}", response_model=CartOut)
def get_cart(user_id: int, db=Depends(get_db)):
    """Get user's cart with all items"""
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Get cart
        cursor.execute("SELECT cart_id, user_id, created_date, total_amount FROM cart WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        
        if not cart:
            # Return empty cart instead of 404
            if cursor:
                cursor.close()
            return {
                "cart_id": 0,
                "user_id": user_id,
                "created_date": None,
                "total_amount": 0.0,
                "cart_items": []
            }
        
        # Get cart items with product details
        cursor.execute("""
            SELECT ci.cart_item_id, ci.cart_id, ci.variant_id, ci.quantity,
                   v.price, v.variant_name,
                   p.product_id, p.product_name
            FROM cart_item ci
            JOIN variant v ON ci.variant_id = v.variant_id
            JOIN product p ON v.product_id = p.product_id
            WHERE ci.cart_id = %s
        """, (cart['cart_id'],))
        items = cursor.fetchall()
        
        if cursor:
            cursor.close()
        
        # Format items to match schema
        formatted_items = []
        if items:
            for item in items:
                formatted_item = {
                    "cart_item_id": item["cart_item_id"],
                    "cart_id": item["cart_id"],
                    "variant_id": item["variant_id"],
                    "quantity": item["quantity"],
                    "price": float(item["price"]),
                    "product_name": item.get("product_name"),
                    "product_id": item.get("product_id"),
                    "variant_name": item.get("variant_name", "")
                }
                formatted_items.append(formatted_item)
        
        result = {
            "cart_id": cart["cart_id"],
            "user_id": cart["user_id"],
            "created_date": cart.get("created_date"),
            "total_amount": float(cart.get("total_amount", 0.0)),
            "cart_items": formatted_items
        }
        
        return result
        
    except HTTPException:
        if cursor:
            cursor.close()
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error retrieving cart: {str(e)}")


@router.put("/update/{cart_item_id}")
def update_cart_item(cart_item_id: int, quantity: int, db=Depends(get_db)):
    """Update cart item quantity"""
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # First, get the cart_id for this item
        cursor.execute("SELECT cart_id FROM cart_item WHERE cart_item_id = %s", (cart_item_id,))
        item = cursor.fetchone()
        
        if not item:
            if cursor:
                cursor.close()
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        cart_id = item['cart_id']
        
        if quantity <= 0:
            cursor.execute("DELETE FROM cart_item WHERE cart_item_id = %s", (cart_item_id,))
        else:
            cursor.execute(
                "UPDATE cart_item SET quantity = %s WHERE cart_item_id = %s",
                (quantity, cart_item_id)
            )
        
        # Recalculate cart total
        cursor.execute("""
            SELECT SUM(ci.quantity * v.price) as total
            FROM cart_item ci
            JOIN variant v ON ci.variant_id = v.variant_id
            WHERE ci.cart_id = %s
        """, (cart_id,))
        total_result = cursor.fetchone()
        new_total = float(total_result['total']) if total_result and total_result['total'] else 0.0
        
        # Update cart total_amount
        cursor.execute(
            "UPDATE cart SET total_amount = %s WHERE cart_id = %s",
            (new_total, cart_id)
        )
        
        db.commit()
        cursor.close()
        
        return {"message": "Cart item updated successfully", "new_total": new_total}
        
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error updating cart: {str(e)}")


@router.delete("/remove/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db=Depends(get_db)):
    """Remove item from cart"""
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Get cart_id before deleting
        cursor.execute("SELECT cart_id FROM cart_item WHERE cart_item_id = %s", (cart_item_id,))
        item = cursor.fetchone()
        
        if not item:
            if cursor:
                cursor.close()
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        cart_id = item['cart_id']
        
        # Delete the item
        cursor.execute("DELETE FROM cart_item WHERE cart_item_id = %s", (cart_item_id,))
        
        # Recalculate cart total
        cursor.execute("""
            SELECT SUM(ci.quantity * v.price) as total
            FROM cart_item ci
            JOIN variant v ON ci.variant_id = v.variant_id
            WHERE ci.cart_id = %s
        """, (cart_id,))
        total_result = cursor.fetchone()
        new_total = float(total_result['total']) if total_result and total_result['total'] else 0.0
        
        # Update cart total_amount
        cursor.execute(
            "UPDATE cart SET total_amount = %s WHERE cart_id = %s",
            (new_total, cart_id)
        )
        
        db.commit()
        cursor.close()
        
        return {"message": "Item removed from cart", "new_total": new_total}
        
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error removing item: {str(e)}")


@router.delete("/clear/{user_id}")
def clear_cart(user_id: int, db=Depends(get_db)):
    """Clear all items from user's cart"""
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        
        if cart:
            cursor.execute("DELETE FROM cart_item WHERE cart_id = %s", (cart['cart_id'],))
            # Set total to 0
            cursor.execute("UPDATE cart SET total_amount = 0 WHERE cart_id = %s", (cart['cart_id'],))
            db.commit()
        
        cursor.close()
        
        return {"message": "Cart cleared successfully", "new_total": 0.0}
        
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error clearing cart: {str(e)}")


@router.get("/delivery-estimate/{user_id}")
def get_delivery_estimate(
    user_id: int,
    delivery_method: str = Query(..., description="home_delivery or store_pickup"),
    city: Optional[str] = Query(None, description="City name for home delivery"),
    db=Depends(get_db)
):
    """
    Calculate estimated delivery days for user's cart
    Based on delivery method, city type, and stock availability
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Get cart
        cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        
        if not cart:
            return {"estimated_days": None, "message": "Cart not found"}
        
        # Get cart items with stock quantities
        cursor.execute(
            """SELECT ci.variant_id, ci.quantity, v.quantity as stock_quantity
               FROM cart_item ci
               JOIN variant v ON ci.variant_id = v.variant_id
               WHERE ci.cart_id = %s""",
            (cart['cart_id'],)
        )
        cart_items = cursor.fetchall()
        
        if not cart_items:
            return {"estimated_days": None, "message": "Cart is empty"}
        
        estimated_days = 0
        has_low_stock = False
        is_main_city = None
        
        if delivery_method == "store_pickup":
            estimated_days = 2
        elif delivery_method == "home_delivery":
            # Check for low stock (quantity < 10)
            has_low_stock = any(item['stock_quantity'] < 10 for item in cart_items)
            
            if not city:
                # Return range-based estimate when no city selected
                main_city_days = 5 + (3 if has_low_stock else 0)
                other_city_days = 7 + (3 if has_low_stock else 0)
                return {
                    "estimated_days": None,
                    "delivery_method": delivery_method,
                    "has_low_stock": has_low_stock,
                    "main_city_estimate": main_city_days,
                    "other_city_estimate": other_city_days,
                    "message": "Select city for exact estimate"
                }
            
            # Check if city is a main city
            cursor.execute(
                "SELECT Is_main_city FROM location WHERE city = %s",
                (city,)
            )
            location = cursor.fetchone()
            
            if not location:
                # Default to non-main city if not found
                base_days = 7
                is_main_city = False
            else:
                is_main_city = location['Is_main_city']
                base_days = 5 if is_main_city else 7
            
            if has_low_stock:
                base_days += 3
            
            estimated_days = base_days
        
        cursor.close()
        
        return {
            "estimated_days": estimated_days,
            "delivery_method": delivery_method,
            "has_low_stock": has_low_stock,
            "is_main_city": is_main_city
        }
        
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error calculating delivery estimate: {str(e)}")
