"""
Delivery Schemas
"""
from pydantic import BaseModel
from datetime import date
from typing import Optional


class DeliveryBase(BaseModel):
    delivery_method: str
    address_id: Optional[int] = None


class DeliveryCreate(BaseModel):
    delivery_method: str  # 'store_pickup' or 'home_delivery'
    address_id: Optional[int] = None


class DeliveryOut(BaseModel):
    delivery_id: int
    order_id: int
    delivery_method: str
    address_id: Optional[int]
    estimated_delivery_date: Optional[date]
    delivery_status: str

    class Config:
        from_attributes = True
