"""
Apply Variant Quantity Trigger
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import text
from app.database import engine

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
    try:
        conn = engine.connect()
        print("Dropping existing variant trigger (if any)...")
        conn.execute(text(trigger_drop))
        conn.commit()

        print("Creating variant quantity trigger...")
        conn.execute(text(trigger_create))
        conn.commit()

        print("✅ Variant quantity trigger created successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Error applying trigger: {e}")
        raise

if __name__ == '__main__':
    apply_trigger()
