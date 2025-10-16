"""
Location Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/locations", tags=["locations"])


class LocationOut(BaseModel):
    city_id: int
    city: str
    zip_code: int = None
    Is_main_city: bool = False

    class Config:
        from_attributes = True


@router.get("/cities", response_model=List[LocationOut])
def get_all_cities(db=Depends(get_db)):
    """
    Get all cities from location table
    """
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM location ORDER BY city")
    cities = cursor.fetchall()
    cursor.close()
    return cities


@router.get("/cities/{city_name}", response_model=LocationOut)
def get_city_by_name(city_name: str, db=Depends(get_db)):
    """
    Get city details by name
    """
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM location WHERE city = %s", (city_name,))
    city = cursor.fetchone()
    cursor.close()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
