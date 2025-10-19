"""
Verify Email Validation Trigger
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection

def verify_trigger():
    """Verify that the email validation trigger exists"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if trigger exists
        cursor.execute("SHOW TRIGGERS WHERE `Trigger` = 'trg_check_email_before_insert'")
        trigger = cursor.fetchone()
        
        if trigger:
            print("✅ Email validation trigger verified successfully!")
            print(f"   Trigger Name: {trigger[0]}")
            print(f"   Event: {trigger[1]}")
            print(f"   Table: {trigger[2]}")
            print(f"   Timing: {trigger[4]}")
            print(f"\n   The trigger will validate email addresses contain '@' symbol")
        else:
            print("❌ Trigger not found in database")
            print("   Run: python database/apply_email_trigger.py")
        
    except Exception as e:
        print(f"❌ Error verifying trigger: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    verify_trigger()
