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
        # Check if product exists
        print(f"DEBUG: Checking if product {product_id} exists...")
        cursor.execute("SELECT product_id FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        print(f"DEBUG: Product {product_id} found, checking orders...")
        
        # Check if product variants exist in orders
        cursor.execute(
            """SELECT COUNT(*) as count 
               FROM order_item oi 
               JOIN variant v ON oi.variant_id = v.variant_id 
               WHERE v.product_id = %s""",
            (product_id,)
        )
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete product: it has {result['count']} order(s). Please archive instead of delete."
            )
        
        print(f"DEBUG: No orders found, deleting variants one by one...")
        # Fetch all variant IDs for this product
        cursor.execute("SELECT variant_id FROM variant WHERE product_id = %s", (product_id,))
        variant_ids = [row['variant_id'] for row in cursor.fetchall()]
        variants_deleted = 0
        for variant_id in variant_ids:
            try:
                # Call the delete_variant logic directly
                # (simulate a request, but pass db and admin context)
                delete_variant(variant_id, db=db, admin=admin)
                variants_deleted += 1
            except HTTPException as ve:
                print(f"DEBUG: Could not delete variant {variant_id}: {ve.detail}")
                # Optionally, you can choose to raise or skip
                continue
        print(f"DEBUG: Deleted {variants_deleted} variants")
        
        # Delete favorites related to this product (if table exists)
        print(f"DEBUG: Attempting to delete favorites...")
        try:
            cursor.execute("DELETE FROM favorite_product WHERE product_id = %s", (product_id,))
            print(f"DEBUG: Deleted favorites successfully")
        except mysql.connector.Error as e:
            # Ignore if table doesn't exist (error 1146)
            print(f"DEBUG: Favorite deletion error: {e.errno} - {e.msg}")
            if e.errno != 1146:
                raise
        
        print(f"DEBUG: Deleting product...")
        # Delete the product
        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        
        print(f"DEBUG: Committing transaction...")
        db.commit()
        print(f"DEBUG: Commit successful!")
        
        return {
            "deleted": True, 
            "product_id": product_id,
            "variants_deleted": variants_deleted,
            "message": "Product and associated data deleted successfully"
        }
    except HTTPException:
        print(f"DEBUG: HTTPException occurred, rolling back...")
        db.rollback()
        raise
    except mysql.connector.Error as e:
        print(f"DEBUG: MySQL Error: {e.errno} - {e.msg}")
        import traceback
        traceback.print_exc()
        db.rollback()
        # Handle foreign key constraint errors
        if e.errno == 1451:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete product: it is referenced in other tables (orders, cart, etc.)"
            )
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        print(f"DEBUG: General Exception: {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
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
        # Check if variant exists in any orders (pre-check before trigger)
        cursor.execute(
            "SELECT COUNT(*) as count FROM order_item WHERE variant_id = %s",
            (variant_id,)
        )
        result = cursor.fetchone()
        if result and result['count'] > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete this variant: This variant is part of existing orders and cannot be removed. Orders must be preserved for record-keeping."
            )
        
        # Delete the variant (trigger will also check for order references)
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
        # Handle trigger error (SQLSTATE 45000)
        if e.errno == 1644:  # Trigger SIGNAL error
            raise HTTPException(
                status_code=400,
                detail="Cannot delete this variant: This variant is part of existing orders and cannot be removed."
            )
        # Handle foreign key constraint error
        elif e.errno == 1451:  # Cannot delete or update a parent row
            raise HTTPException(
                status_code=400,
                detail="Cannot delete this variant: This variant is part of existing orders and cannot be removed."
            )
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting variant: {str(e)}")
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


@router.put("/orders/{order_id}/payment-status", response_model=dict)
def update_payment_status(
    order_id: int,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin=Depends(get_admin_user)
):
    """
    Update payment status to 'completed' for an order.
    Primarily used for Cash on Delivery (COD) orders.
    """
    cursor = db.cursor(dictionary=True)
    try:
        # Check if order exists
        cursor.execute("SELECT order_id FROM orders WHERE order_id = %s", (order_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Check if payment record exists
        cursor.execute("SELECT payment_id, payment_status FROM payment WHERE order_id = %s", (order_id,))
        payment = cursor.fetchone()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found for this order")
        
        if payment['payment_status'] == 'completed':
            return {
                "success": True,
                "message": "Payment is already marked as completed",
                "order_id": order_id,
                "payment_status": "completed"
            }
        
        # Update payment status to completed
        cursor.execute(
            "UPDATE payment SET payment_status = 'completed' WHERE order_id = %s",
            (order_id,)
        )
        db.commit()
        
        return {
            "success": True,
            "message": f"Payment status updated to completed for order {order_id}",
            "order_id": order_id,
            "payment_status": "completed"
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating payment status: {str(e)}")
    finally:
        cursor.close()
