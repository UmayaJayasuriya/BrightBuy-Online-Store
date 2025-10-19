"""
Favorite Product Schemas
Pydantic models for request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FavoriteBase(BaseModel):
    """Base favorite schema"""
    product_id: int


class FavoriteCreate(FavoriteBase):
    """Schema for creating a favorite"""
    pass


class FavoriteOut(BaseModel):
    """Schema for favorite output"""
    favorite_id: int
    user_id: int
    product_id: int
    created_at: datetime
    
    # Product details (joined from product table)
    product_name: Optional[str] = None
    description: Optional[str] = None
    category_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class FavoriteResponse(BaseModel):
    """Response schema for favorite operations"""
    message: str
    favorite_id: Optional[int] = None
