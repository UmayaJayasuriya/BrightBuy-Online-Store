# app/schemas/category.py
from pydantic import BaseModel
from typing import Optional

class CategoryOut(BaseModel):
    category_id: int
    category_name: str
    parent_category_id: Optional[int]

    class Config:
        from_attributes = True
