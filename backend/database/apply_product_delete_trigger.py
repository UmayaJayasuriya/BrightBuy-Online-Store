"""
Apply Product Delete Protection Trigger
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import text
from app.database import engine

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
    try:
        conn = engine.connect()
        print("Dropping existing product delete trigger (if any)...")
        conn.execute(text(TRIGGER_DROP))
        conn.commit()

        print("Creating product delete protection trigger...")
        conn.execute(text(TRIGGER_CREATE))
        conn.commit()

        print("✅ Product delete trigger created successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Error applying product delete trigger: {e}")
        raise

if __name__ == "__main__":
    apply_trigger()
