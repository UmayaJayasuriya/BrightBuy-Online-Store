from pydantic import BaseModel
from typing import Optional, List
from app.schemas.variant import VariantCreate

# Category info for product response
class CategoryInfo(BaseModel):
    category_id: int
    category_name: str
    
    class Config:
        from_attributes = True

# Product response schema
class ProductOut(BaseModel):
    product_id: int
    product_name: str
    category_id: int
    description: Optional[str]
    category: Optional[CategoryInfo] = None
    
    class Config:
        from_attributes = True

# Product creation schema (for future use)
class ProductCreate(BaseModel):
    product_name: str
    category_id: int
    description: Optional[str] = None
    variants: Optional[List[VariantCreate]] = None
