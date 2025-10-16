from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("cart.cart_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Relationships
    # cart = relationship("Cart")  # optional
    # user = relationship("User")  # optional
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_item"

    order_item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")


class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    payment_method = Column(String(30), nullable=False)
    payment_status = Column(String(30), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="payments")


class Delivery(Base):
    __tablename__ = "delivery"

    delivery_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=True)
    address_id = Column(Integer, ForeignKey("address.address_id"), nullable=True)
    delivery_method = Column(String(50))
    estimated_delivery_date = Column(DateTime, nullable=True)
    delivery_status = Column(String(20))
