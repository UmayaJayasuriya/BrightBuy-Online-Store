"""
Admin-specific Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Admin Dashboard schemas
class DashboardStats(BaseModel):
    total_users: int
    total_products: int
    total_orders: int
    total_revenue: float
    recent_orders: int
    low_stock_products: int

class UserStats(BaseModel):
    new_users_this_month: int
    active_users: int
    admin_users: int

# User Management schemas
class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    user_type: Optional[str] = None

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    name: str
    password: str
    user_type: str = "customer"

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    name: str
    user_type: str
    is_admin: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Product Management schemas
class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    # Admin UI edits price/stock at product level; we map to first/all variants under the hood
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class ProductCreate(BaseModel):
    product_name: str
    description: str
    category_id: int
    stock_quantity: int = 0

class AdminProductResponse(BaseModel):
    product_id: int
    product_name: str
    description: str
    category_id: int
    # Derived from first variant (or 0 if none)
    price: float
    stock_quantity: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Category Management schemas
class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None

class CategoryCreate(BaseModel):
    category_name: str
    description: Optional[str] = None

# Order Management schemas
class OrderStatusUpdate(BaseModel):
    status: str  # e.g., "pending", "confirmed", "shipped", "delivered", "cancelled"

class AdminOrderResponse(BaseModel):
    order_id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    user_name: Optional[str] = None
    user_email: Optional[str] = None

    class Config:
        from_attributes = True

# Analytics schemas
class SalesAnalytics(BaseModel):
    daily_sales: List[dict]
    monthly_sales: List[dict]
    top_products: List[dict]
    top_categories: List[dict]

class UserAnalytics(BaseModel):
    user_registrations: List[dict]
    user_activity: List[dict]
    user_demographics: dict