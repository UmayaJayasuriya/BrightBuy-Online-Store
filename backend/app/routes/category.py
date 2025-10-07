# app/routes/category.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.category import Category
from app.schemas.category import CategoryOut
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CategoryOut])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
