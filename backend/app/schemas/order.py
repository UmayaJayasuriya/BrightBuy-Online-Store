"""
Order Schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemOut(BaseModel):
    order_item_id: int
    order_id: int
    variant_id: Optional[int] = None
    quantity: int
    price: float
    variant_name: Optional[str] = None
    product_name: Optional[str] = None
    product_id: Optional[int] = None

    class Config:
        from_attributes = True


class AddressDetails(BaseModel):
    house_number: int
    street: str
    city: str
    state: str


class CardDetails(BaseModel):
    card_number: str
    card_name: str
    expiry_date: str
    cvv: str


class CreateOrderRequest(BaseModel):
    user_id: int
    payment_method: str  # 'card' or 'cod'
    delivery_method: str  # 'store_pickup' or 'home_delivery'
    address_id: Optional[int] = None  # Required for home_delivery
    address_details: Optional[AddressDetails] = None  # New address details if creating new address
    card_details: Optional[CardDetails] = None  # Card details for card payment


class OrderOut(BaseModel):
    order_id: int
    cart_id: Optional[int] = None
    user_id: int
    order_date: datetime
    total_amount: float
    estimated_delivery_date: Optional[str] = None  # ISO date string
    estimated_delivery_days: Optional[int] = None  # Number of days
    order_items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
