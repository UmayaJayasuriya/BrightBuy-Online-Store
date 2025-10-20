"""
Apply CVV Validation Trigger
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection

trigger_drop = "DROP TRIGGER IF EXISTS check_cvv_length;"

trigger_create = """
CREATE TRIGGER check_cvv_length
BEFORE INSERT ON card
FOR EACH ROW
BEGIN
    IF LENGTH(NEW.CVV) != 3 OR NEW.CVV REGEXP '[^0-9]' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CVV must be exactly 3 digits';
    END IF;
END;
"""


def apply_trigger():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Dropping existing CVV trigger (if any)...")
        cursor.execute(trigger_drop)
        conn.commit()

        print("Creating CVV validation trigger...")
        cursor.execute(trigger_create)
        conn.commit()

        print(" CVV validation trigger created successfully!")
    except Exception as e:
        print(f" Error applying CVV trigger: {e}")
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
