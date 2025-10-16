"""
Verify Email Validation Trigger
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import text
from app.database import engine

def verify_trigger():
    """Verify that the email validation trigger exists"""
    try:
        conn = engine.connect()
        
        # Check if trigger exists
        result = conn.execute(text("SHOW TRIGGERS WHERE `Trigger` = 'trg_check_email_before_insert'"))
        trigger = result.fetchone()
        
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
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verifying trigger: {str(e)}")

if __name__ == "__main__":
    verify_trigger()
