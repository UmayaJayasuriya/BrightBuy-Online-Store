"""
Apply Delivery Status Trigger
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import text
from app.database import engine

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
    try:
        conn = engine.connect()
        print("Dropping existing delivery status trigger (if any)...")
        conn.execute(text(trigger_drop))
        conn.commit()

        print("Creating delivery status trigger...")
        conn.execute(text(trigger_create))
        conn.commit()

        print("✅ Delivery status trigger created successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Error applying trigger: {e}")
        raise

if __name__ == '__main__':
    apply_trigger()
