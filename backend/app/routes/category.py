# app/routes/category.py
from fastapi import APIRouter, Depends, HTTPException
import mysql.connector
from app.database import get_db
from app.schemas.category import CategoryOut
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryOut])
def get_all_categories(db: mysql.connector.MySQLConnection = Depends(get_db)):
    """Get all categories (skipping first 3)"""
    cursor = db.cursor(dictionary=True)
    try:
        # Get all categories ordered by ID and skip the first 3
        query = """
            SELECT category_id, category_name, parent_category_id 
            FROM category 
            ORDER BY category_id 
            LIMIT 18446744073709551615 OFFSET 3
        """
        cursor.execute(query)
        categories = cursor.fetchall()
        cursor.close()
        return categories
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
