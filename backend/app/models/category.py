# app/models/category.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100))
    parent_category_id = Column(Integer, ForeignKey("category.category_id"), nullable=True)
