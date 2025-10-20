from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional
import mysql.connector
from app.database import get_db
from app.security import get_admin_user
from app.schemas.product import ProductCreate
from app.schemas.variant import VariantCreate

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[dict])
def list_users(db: mysql.connector.MySQLConnection = Depends(get_db), admin=Depends(get_admin_user)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, user_name, email, name, user_type FROM user ORDER BY user_id DESC")
        users = cursor.fetchall()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.get("/orders", response_model=List[dict])
def list_orders(db: mysql.connector.MySQLConnection = Depends(get_db), admin=Depends(get_admin_user)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT o.order_id, o.user_id, o.order_date, o.total_amount,
                   d.delivery_status, p.payment_method, p.payment_status
            FROM orders o
            LEFT JOIN delivery d ON o.order_id = d.order_id
            LEFT JOIN payment p ON o.order_id = p.order_id
            ORDER BY o.order_date DESC
            """
        )
        orders = cursor.fetchall()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.get("/orders/{order_id}/items", response_model=List[dict])
def get_order_items(order_id: int, db: mysql.connector.MySQLConnection = Depends(get_db), admin=Depends(get_admin_user)):
    """Get all items (products/variants) for a specific order"""
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT oi.order_item_id, oi.order_id, oi.quantity, oi.price,
                   v.variant_id, v.variant_name, v.SKU,
                   p.product_id, p.product_name
            FROM order_item oi
            LEFT JOIN variant v ON oi.variant_id = v.variant_id
            LEFT JOIN product p ON v.product_id = p.product_id
            WHERE oi.order_id = %s
            """,
            (order_id,)
        )
        items = cursor.fetchall()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.post("/products", response_model=dict, status_code=201)
def create_product(
    product: ProductCreate = Body(...),
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin=Depends(get_admin_user)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO product (product_name, category_id, description) VALUES (%s, %s, %s)",
            (product.product_name, product.category_id, product.description)
        )
        db.commit()
        product_id = cursor.lastrowid
        # If variants provided, insert them
        if product.variants:
            for v in product.variants:
                cursor.execute(
                    "INSERT INTO variant (variant_name, product_id, price, quantity, SKU) VALUES (%s, %s, %s, %s, %s)",
                    (v.variant_name, product_id, v.price, v.quantity, v.SKU)
                )
            db.commit()
        return {"product_id": product_id, "product_name": product.product_name, "category_id": product.category_id, "description": product.description}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.delete("/products/{product_id}", response_model=dict)
def delete_product(
    product_id: int,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin=Depends(get_admin_user)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        db.commit()
        return {"deleted": True, "product_id": product_id}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.put("/variants/{variant_id}/quantity", response_model=dict)
def update_variant_quantity(
    variant_id: int,
    quantity: int,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin=Depends(get_admin_user)
):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("UPDATE variant SET quantity = %s WHERE variant_id = %s", (quantity, variant_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Variant not found")
        db.commit()
        return {"updated": True, "variant_id": variant_id, "quantity": quantity}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.delete("/variants/{variant_id}", response_model=dict)
def delete_variant(
    variant_id: int,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin=Depends(get_admin_user)
):
    cursor = db.cursor(dictionary=True)
    try:
        # Check if variant exists in any orders
        cursor.execute(
            "SELECT COUNT(*) as count FROM order_item WHERE variant_id = %s",
            (variant_id,)
        )
        result = cursor.fetchone()
        if result and result['count'] > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete variant: it is referenced in existing orders"
            )
        # Delete the variant
        cursor.execute("DELETE FROM variant WHERE variant_id = %s", (variant_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Variant not found")
        db.commit()
        return {"deleted": True, "variant_id": variant_id}
    except HTTPException:
        db.rollback()
        raise
    except mysql.connector.Error as e:
        db.rollback()
        # Handle foreign key constraint error
        if e.errno == 1451:  # Cannot delete or update a parent row
            raise HTTPException(
                status_code=400,
                detail="Cannot delete variant: it is referenced in existing orders"
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@router.post("/products/{product_id}/variants", response_model=dict, status_code=201)
def add_variant_to_product(
    product_id: int,
    variant: VariantCreate = Body(...),
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin=Depends(get_admin_user)
):
    """Add a new variant to an existing product."""
    cursor = db.cursor(dictionary=True)
    try:
        # Optionally ensure product exists
        cursor.execute("SELECT product_id FROM product WHERE product_id = %s", (product_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute(
            """
            INSERT INTO variant (variant_name, product_id, price, quantity, SKU)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (variant.variant_name, product_id, variant.price, variant.quantity, variant.SKU)
        )
        db.commit()
        variant_id = cursor.lastrowid
        return {
            "variant_id": variant_id,
            "variant_name": variant.variant_name,
            "product_id": product_id,
            "price": variant.price,
            "quantity": variant.quantity,
            "SKU": variant.SKU,
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

