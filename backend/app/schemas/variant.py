from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

# Variant Attribute schema
class VariantAttributeOut(BaseModel):
    attribute_name: str
    value: Optional[str] = None
    
    class Config:
        from_attributes = True


# Variant creation schema
class VariantCreate(BaseModel):
    variant_name: str
    price: float
    quantity: int
    SKU: Optional[str] = None


# Variant schema
class VariantOut(BaseModel):
    variant_id: int
    variant_name: str
    product_id: int
    price: Decimal
    quantity: int
    SKU: Optional[str] = None
    attributes: List[VariantAttributeOut] = []
    
    class Config:
        from_attributes = True


# Product with variants schema
class ProductWithVariantsOut(BaseModel):
    product_id: int
    product_name: str
    category_id: int
    description: Optional[str]
    category: Optional[dict] = None
    variants: List[VariantOut] = []
    
    class Config:
        from_attributes = True
