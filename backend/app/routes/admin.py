"""
Admin routes for managing the system
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List
from app.database import get_db
from app.models.user import User, USER_ROLES
from app.models.product import Product
from app.models.category import Category
from app.models.variant import Variant
from app.models.order import Order, Payment
from app.utils.auth import get_admin_user, get_super_admin_user
from app.schemas.admin import (
    DashboardStats, UserUpdate, UserResponse, ProductUpdate, 
    AdminProductResponse, CategoryUpdate, CategoryCreate, UserCreate
)
import bcrypt

router = APIRouter(prefix="/admin", tags=["Admin"])

# Category Management routes
@router.get("/categories")
def get_all_categories_admin(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all categories for admin view"""
    try:
        categories = db.query(Category).offset(skip).limit(limit).all()
        return [
            {
                "category_id": c.category_id,
                "category_name": c.category_name,
                "description": getattr(c, "description", None)
            }
            for c in categories
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

# Dashboard routes
@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    total_users = db.query(User).count()
    total_products = db.query(Product).count()

    # Mock data for orders and revenue (replace with actual models when available)
    try:
        total_orders = db.query(Order).count()
        total_revenue = float(db.query(func.coalesce(func.sum(Order.total_amount), 0)).scalar() or 0.0)
    except Exception:
        total_orders = 0
        total_revenue = 0.0

    recent_orders = 0  # Optional: implement based on order_date within last N days

    # Compute low stock by summing variant quantities per product (< 10)
    low_stock_products = 0
    try:
        products = db.query(Product).all()
        for p in products:
            variants = db.query(Variant).filter(Variant.product_id == p.product_id).all()
            total_qty = sum(int(v.quantity or 0) for v in variants)
            if total_qty < 10:
                low_stock_products += 1
    except Exception:
        low_stock_products = 0

    return DashboardStats(
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        recent_orders=recent_orders,
        low_stock_products=low_stock_products
    )

from typing import List as _List
from app.schemas.admin import AdminOrderResponse as _AdminOrderResponse

@router.get("/orders", response_model=_List[_AdminOrderResponse])
def get_all_orders_admin(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all orders for admin view"""
    try:
        orders = db.query(Order).order_by(Order.order_date.desc()).offset(skip).limit(limit).all()
        result = []
        for o in orders:
            # Try to get payment status
            pay = db.query(Payment).filter(Payment.order_id == o.order_id).order_by(Payment.payment_date.desc()).first()
            status = pay.payment_status if pay and getattr(pay, 'payment_status', None) else "pending"
            # Fetch user info via user_id
            user = db.query(User).filter(User.user_id == o.user_id).first()
            result.append({
                "order_id": o.order_id,
                "user_id": o.user_id,
                "total_amount": float(o.total_amount or 0),
                "status": status,
                "created_at": o.order_date,
                "user_name": user.user_name if user else None,
                "user_email": user.email if user else None
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

# User Management routes
@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all users (admin only)"""
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return [
            UserResponse(
                user_id=user.user_id,
                user_name=user.user_name,
                email=user.email,
                name=user.name,
                user_type=user.user_type,
                is_admin=user.has_admin_privileges()
            ) for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.post("/users", response_model=UserResponse)
def create_user_admin(
    user_data: UserCreate,
    admin_user: User = Depends(get_super_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new user (super admin only)"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Hash password
        password_bytes = user_data.password.encode('utf-8')[:72]
        hashed_pw = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        # Create new user
        new_user = User(
            user_name=user_data.user_name,
            email=user_data.email,
            name=user_data.name,
            password_hash=hashed_pw,
            user_type=user_data.user_type
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return UserResponse(
            user_id=new_user.user_id,
            user_name=new_user.user_name,
            email=new_user.email,
            name=new_user.name,
            user_type=new_user.user_type,
            is_admin=new_user.has_admin_privileges()
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update user information"""
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update only provided fields
        for field, value in user_data.dict(exclude_unset=True).items():
            if field == "user_type" and not admin_user.is_admin():
                # Only super admins can change user types
                raise HTTPException(status_code=403, detail="Only super admins can change user types")
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return UserResponse(
            user_id=user.user_id,
            user_name=user.user_name,
            email=user.email,
            name=user.name,
            user_type=user.user_type,
            is_admin=user.has_admin_privileges()
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin_user: User = Depends(get_super_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a user (super admin only)"""
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prevent deleting yourself
        if user.user_id == admin_user.user_id:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        db.delete(user)
        db.commit()
        
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

# Product Management routes
@router.get("/products", response_model=List[AdminProductResponse])
def get_all_products_admin(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all products with admin details"""
    try:
        products = db.query(Product).offset(skip).limit(limit).all()
        result = []
        for product in products:
            # derive price and stock from variants
            variants = db.query(Variant).filter(Variant.product_id == product.product_id).all()
            if variants:
                # choose min price and sum quantities for display
                price = float(min([float(v.price) for v in variants if v.price is not None]))
                stock_quantity = int(sum([int(v.quantity or 0) for v in variants]))
            else:
                price = 0.0
                stock_quantity = 0

            result.append(AdminProductResponse(
                product_id=product.product_id,
                product_name=product.product_name,
                description=product.description or "",
                category_id=product.category_id,
                price=price,
                stock_quantity=stock_quantity
            ))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

@router.put("/products/{product_id}")
def update_product_admin(
    product_id: int,
    product_data: ProductUpdate,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update product information"""
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update only provided fields
        data = product_data.dict(exclude_unset=True)

        # Update product core fields
        for field in ["product_name", "description", "category_id"]:
            if field in data:
                setattr(product, field, data[field])

        # If price or stock updates are provided, map them to variants
        if "price" in data or "stock_quantity" in data:
            variants = db.query(Variant).filter(Variant.product_id == product.product_id).all()
            # Ensure at least one variant exists to hold product-level edits
            if not variants:
                default_variant = Variant(
                    variant_name=f"Default {product.product_name}",
                    product_id=product.product_id,
                    price=data.get("price", 0.0) if data.get("price") is not None else 0.0,
                    quantity=data.get("stock_quantity", 0) if data.get("stock_quantity") is not None else 0,
                    SKU=None
                )
                db.add(default_variant)
            else:
                if "price" in data and data["price"] is not None:
                    for v in variants:
                        v.price = data["price"]
                if "stock_quantity" in data and data["stock_quantity"] is not None:
                    # Set stock on the first variant (simple strategy)
                    variants[0].quantity = data["stock_quantity"]
        
        db.commit()
        db.refresh(product)
        
        return {"message": "Product updated successfully", "product_id": product.product_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

@router.delete("/products/{product_id}")
def delete_product_admin(
    product_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a product"""
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(product)
        db.commit()
        
        return {"message": "Product deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")

# Category Management routes
@router.post("/categories")
def create_category_admin(
    category_data: CategoryCreate,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new category"""
    try:
        new_category = Category(
            category_name=category_data.category_name,
            description=getattr(category_data, 'description', None)
        )
        
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        
        return {"message": "Category created successfully", "category_id": new_category.category_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating category: {str(e)}")

@router.put("/categories/{category_id}")
def update_category_admin(
    category_id: int,
    category_data: CategoryUpdate,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update category information"""
    try:
        category = db.query(Category).filter(Category.category_id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Update only provided fields
        for field, value in category_data.dict(exclude_unset=True).items():
            setattr(category, field, value)
        
        db.commit()
        db.refresh(category)
        
        return {"message": "Category updated successfully", "category_id": category.category_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating category: {str(e)}")

@router.delete("/categories/{category_id}")
def delete_category_admin(
    category_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a category"""
    try:
        category = db.query(Category).filter(Category.category_id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Check if category has products
        products_count = db.query(Product).filter(Product.category_id == category_id).count()
        if products_count > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete category. It has {products_count} products."
            )
        
        db.delete(category)
        db.commit()
        
        return {"message": "Category deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting category: {str(e)}")