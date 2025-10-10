from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    description = Column(String(255), nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    variants = relationship("Variant", back_populates="product")
