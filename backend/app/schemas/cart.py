"""
Cart Schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CartItemCreate(BaseModel):
    variant_id: int
    quantity: int = 1


class CartItemOut(BaseModel):
    cart_item_id: int
    cart_id: int
    variant_id: int
    quantity: int
    price: float
    variant_name: Optional[str] = None
    product_name: Optional[str] = None
    product_id: Optional[int] = None

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    cart_id: int
    user_id: int
    created_date: Optional[datetime] = None
    total_amount: float
    cart_items: List[CartItemOut] = []

    class Config:
        from_attributes = True



class AddToCartRequest(BaseModel):
    user_id: int
    variant_id: int
    quantity: int = 1
