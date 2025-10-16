"""
Card Payment Schemas
Pydantic models for card payment data validation
"""
from pydantic import BaseModel
from typing import Optional


class CardDetails(BaseModel):
    """Card details for payment"""
    card_number: str
    card_name: str
    expiry_date: str
    cvv: str


class CardOut(BaseModel):
    """Card output schema"""
    card_id: int
    order_id: int
    card_number: str
    card_name: str
    expiry_date: str
    
    class Config:
        from_attributes = True
