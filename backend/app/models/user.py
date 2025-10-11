from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(50))
    password_hash = Column(String(100))
    user_type = Column(String(30))
    address_id = Column(Integer, ForeignKey("address.address_id", ondelete="SET NULL"), nullable=True)

    address = relationship("Address", back_populates="users")
    carts = relationship("Cart", back_populates="user")

class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer)
    house_number = Column(Integer)
    street = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))

    users = relationship("User", back_populates="address")
