from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# User role constants
USER_ROLES = {
    "ADMIN": "admin",
    "CUSTOMER": "customer",
    "MANAGER": "manager"
}

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

    def is_admin(self) -> bool:
        """Check if user is an admin"""
        return self.user_type == USER_ROLES["ADMIN"]
    
    def is_manager(self) -> bool:
        """Check if user is a manager"""
        return self.user_type == USER_ROLES["MANAGER"]
    
    def has_admin_privileges(self) -> bool:
        """Check if user has admin or manager privileges"""
        return self.user_type in [USER_ROLES["ADMIN"], USER_ROLES["MANAGER"]]

class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer)
    house_number = Column(Integer)
    street = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))

    users = relationship("User", back_populates="address")
