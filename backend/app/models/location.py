from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Location(Base):
    __tablename__ = "location"

    city_id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False)
    zip_code = Column(Integer)
    Is_main_city = Column(Boolean)
