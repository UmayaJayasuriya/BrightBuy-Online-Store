"""
Apply Email Validation Trigger
Run this script to create the email validation trigger in the database
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection

def apply_email_validation_trigger():
    """Apply email validation trigger to User table"""
    
    trigger_sql = """
DROP TRIGGER IF EXISTS trg_check_email_before_insert;
"""
    
    trigger_create = """
CREATE TRIGGER trg_check_email_before_insert
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Please enter a valid email address. It must include the "@" symbol (e.g., name@example.com).';
    END IF;
END;
"""
    
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Drop existing trigger if it exists
        print("Dropping existing trigger (if any)...")
        cursor.execute(trigger_sql)
        conn.commit()
        
        # Create the trigger
        print("Creating email validation trigger...")
        cursor.execute(trigger_create)
        conn.commit()
        
        print("✅ Email validation trigger created successfully!")
        print("   - Trigger: trg_check_email_before_insert")
        print("   - Validates: Email must contain '@' symbol")
        
    except Exception as e:
        print(f"❌ Error creating trigger: {str(e)}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    apply_email_validation_trigger()
