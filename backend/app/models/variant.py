from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Variant(Base):
    __tablename__ = "variant"

    variant_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    variant_name = Column(String(50), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, default=0)
    SKU = Column(String(50))
    
    # Relationships
    product = relationship("Product", back_populates="variants")
    attribute_values = relationship("VariantAttributeValue", back_populates="variant")


class VariantAttribute(Base):
    __tablename__ = "variant_attribute"

    attribute_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    attribute_name = Column(String(20), nullable=False)
    
    # Relationship
    values = relationship("VariantAttributeValue", back_populates="attribute")


class VariantAttributeValue(Base):
    __tablename__ = "variant_attribute_value"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey("variant.variant_id"), nullable=False)
    attribute_id = Column(Integer, ForeignKey("variant_attribute.attribute_id"), nullable=False)
    value = Column(String(50), nullable=False)
    
    # Relationships
    variant = relationship("Variant", back_populates="attribute_values")
    attribute = relationship("VariantAttribute", back_populates="values")
