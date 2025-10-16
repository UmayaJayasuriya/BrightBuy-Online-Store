"""
Payment Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaymentBase(BaseModel):
    payment_method: str
    payment_status: str


class PaymentCreate(BaseModel):
    payment_method: str  # 'card' or 'cod'


class PaymentOut(BaseModel):
    payment_id: int
    order_id: int
    payment_method: str
    payment_status: str
    payment_date: datetime

    class Config:
        from_attributes = True
