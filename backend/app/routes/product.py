from fastapi import APIRouter, Depends, HTTPException, Query
import mysql.connector
from typing import List, Optional
from app.database import get_db
from app.schemas.product import ProductOut
from app.schemas.variant import ProductWithVariantsOut

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductOut])
def get_products(
    category_id: Optional[int] = Query(None),
    category_name: Optional[str] = Query(None),
    db: mysql.connector.MySQLConnection = Depends(get_db)
):
    cursor = db.cursor(dictionary=True)
    try:
        # Build query to get products with category info
        base_query = """
            SELECT 
                p.product_id, 
                p.product_name, 
                p.category_id, 
                p.description,
                c.category_id as cat_id,
                c.category_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.category_id
        """
        
        if category_id:
            cursor.execute(base_query + " WHERE p.category_id = %s", (category_id,))
        elif category_name:
            cursor.execute(base_query + " WHERE c.category_name = %s", (category_name,))
        else:
            cursor.execute(base_query)
        
        products = cursor.fetchall()
        cursor.close()
        
        # Format response to match schema
        result = []
        for p in products:
            product_dict = {
                "product_id": p["product_id"],
                "product_name": p["product_name"],
                "category_id": p["category_id"],
                "description": p["description"],
                "category": {
                    "category_id": p["cat_id"],
                    "category_name": p["category_name"]
                } if p.get("cat_id") else None
            }
            result.append(product_dict)
        
        return result
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{product_id}/variants/", response_model=ProductWithVariantsOut)
def get_product_with_variants(product_id: int, db: mysql.connector.MySQLConnection = Depends(get_db)):
    """Get a specific product with all its variants"""
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Get product info
        cursor.execute("""
            SELECT 
                p.product_id, 
                p.product_name, 
                p.category_id, 
                p.description,
                c.category_id as cat_id,
                c.category_name
            FROM product p
            LEFT JOIN category c ON p.category_id = c.category_id
            WHERE p.product_id = %s
        """, (product_id,))
        product = cursor.fetchone()
        
        if not product:
            cursor.close()
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get variants for this product
        cursor.execute("""
            SELECT 
                variant_id, 
                variant_name,
                product_id, 
                price, 
                quantity,
                SKU
            FROM variant 
            WHERE product_id = %s
        """, (product_id,))
        variants = cursor.fetchall()
        
        cursor.close()
        
        # Format response
        result = {
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category_id": product["category_id"],
            "description": product["description"],
            "category": {
                "category_id": product["cat_id"],
                "category_name": product["category_name"]
            } if product.get("cat_id") else None,
            "variants": variants
        }
        
        return result
    except HTTPException:
        if cursor:
            cursor.close()
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
