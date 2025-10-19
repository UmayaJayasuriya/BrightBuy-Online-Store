"""
Apply Variant Quantity Trigger
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection

trigger_drop = "DROP TRIGGER IF EXISTS check_variant_quantity;"

trigger_create = """
CREATE TRIGGER check_variant_quantity
BEFORE UPDATE ON variant
FOR EACH ROW
BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Quantity cannot be negative';
    END IF;
END;
"""


def apply_trigger():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Dropping existing variant trigger (if any)...")
        cursor.execute(trigger_drop)
        conn.commit()

        print("Creating variant quantity trigger...")
        cursor.execute(trigger_create)
        conn.commit()

        print("✅ Variant quantity trigger created successfully!")
    except Exception as e:
        print(f"❌ Error applying trigger: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    apply_trigger()
