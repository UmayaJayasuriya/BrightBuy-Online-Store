"""
Apply Delivery Status Trigger
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection

trigger_drop = "DROP TRIGGER IF EXISTS set_default_delivery_status;"

trigger_create = """
CREATE TRIGGER set_default_delivery_status
BEFORE INSERT ON Delivery
FOR EACH ROW
BEGIN
    IF NEW.delivery_status IS NULL THEN
        SET NEW.delivery_status = 'Pending';
    END IF;
END;
"""


def apply_trigger():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Dropping existing delivery status trigger (if any)...")
        cursor.execute(trigger_drop)
        conn.commit()

        print("Creating delivery status trigger...")
        cursor.execute(trigger_create)
        conn.commit()

        print("✅ Delivery status trigger created successfully!")
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
