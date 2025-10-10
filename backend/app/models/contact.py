"""
Contact Model
"""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Contact(Base):
    __tablename__ = "contact"

    contact_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject_name = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
