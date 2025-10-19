"""
Favorite Product Routes - MySQL Connector
Handles user favorite/wishlist products
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.favorite import FavoriteCreate, FavoriteOut, FavoriteResponse
from typing import List
from datetime import datetime

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/{user_id}", response_model=List[FavoriteOut])
def get_user_favorites(user_id: int, db=Depends(get_db)):
    """
    Get all favorite products for a user
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(
            """SELECT f.favorite_id, f.user_id, f.product_id, f.created_at,
                      p.product_name, p.description, c.category_name
               FROM favorite_product f
               JOIN product p ON f.product_id = p.product_id
               LEFT JOIN category c ON p.category_id = c.category_id
               WHERE f.user_id = %s
               ORDER BY f.created_at DESC""",
            (user_id,)
        )
        
        favorites = cursor.fetchall()
        cursor.close()
        
        return favorites
        
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error fetching favorites: {str(e)}")


@router.post("/{user_id}", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(user_id: int, favorite: FavoriteCreate, db=Depends(get_db)):
    """
    Add a product to user's favorites
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Check if already in favorites
        cursor.execute(
            "SELECT favorite_id FROM favorite_product WHERE user_id = %s AND product_id = %s",
            (user_id, favorite.product_id)
        )
        
        existing = cursor.fetchone()
        if existing:
            cursor.close()
            return FavoriteResponse(
                message="Product already in favorites",
                favorite_id=existing['favorite_id']
            )
        
        # Check if product exists
        cursor.execute("SELECT product_id FROM product WHERE product_id = %s", (favorite.product_id,))
        product = cursor.fetchone()
        
        if not product:
            cursor.close()
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Insert favorite
        cursor.execute(
            """INSERT INTO favorite_product (user_id, product_id, created_at)
               VALUES (%s, %s, %s)""",
            (user_id, favorite.product_id, datetime.now())
        )
        
        db.commit()
        favorite_id = cursor.lastrowid
        cursor.close()
        
        return FavoriteResponse(
            message="Product added to favorites",
            favorite_id=favorite_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error adding favorite: {str(e)}")


@router.delete("/{user_id}/{product_id}", response_model=FavoriteResponse)
def remove_favorite(user_id: int, product_id: int, db=Depends(get_db)):
    """
    Remove a product from user's favorites
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Check if favorite exists
        cursor.execute(
            "SELECT favorite_id FROM favorite_product WHERE user_id = %s AND product_id = %s",
            (user_id, product_id)
        )
        
        favorite = cursor.fetchone()
        if not favorite:
            cursor.close()
            raise HTTPException(status_code=404, detail="Favorite not found")
        
        # Delete favorite
        cursor.execute(
            "DELETE FROM favorite_product WHERE user_id = %s AND product_id = %s",
            (user_id, product_id)
        )
        
        db.commit()
        cursor.close()
        
        return FavoriteResponse(message="Product removed from favorites")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error removing favorite: {str(e)}")


@router.get("/check/{user_id}/{product_id}")
def check_favorite(user_id: int, product_id: int, db=Depends(get_db)):
    """
    Check if a product is in user's favorites
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT favorite_id FROM favorite_product WHERE user_id = %s AND product_id = %s",
            (user_id, product_id)
        )
        
        favorite = cursor.fetchone()
        cursor.close()
        
        return {
            "is_favorite": favorite is not None,
            "favorite_id": favorite['favorite_id'] if favorite else None
        }
        
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error checking favorite: {str(e)}")
