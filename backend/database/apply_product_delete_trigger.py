"""
Apply Product Delete Protection Trigger
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection

TRIGGER_DROP = "DROP TRIGGER IF EXISTS prevent_product_delete_if_in_order;"

TRIGGER_CREATE = """
CREATE TRIGGER prevent_product_delete_if_in_order
BEFORE DELETE ON product
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM variant v
        JOIN order_item oi ON oi.variant_id = v.variant_id
        WHERE v.product_id = OLD.product_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete product: it is referenced in an order.';
    END IF;
END;
"""

def apply_trigger():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Dropping existing product delete trigger (if any)...")
        cursor.execute(TRIGGER_DROP)
        conn.commit()

        print("Creating product delete protection trigger...")
        cursor.execute(TRIGGER_CREATE)
        conn.commit()

        print("✅ Product delete trigger created successfully!")
    except Exception as e:
        print(f"❌ Error applying product delete trigger: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    apply_trigger()
