"""
Verify CVV Validation Trigger
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import text
from app.database import engine


def verify_trigger():
    try:
        conn = engine.connect()
        result = conn.execute(text("SHOW TRIGGERS WHERE `Trigger` = 'check_cvv_length'"))
        trigger = result.fetchone()
        if trigger:
            print("✅ CVV trigger verified!")
            print(f"   Name: {trigger[0]}")
            print(f"   Event: {trigger[1]}")
            print(f"   Table: {trigger[2]}")
            print(f"   Timing: {trigger[4]}")
        else:
            print("❌ CVV trigger not found")
        conn.close()
    except Exception as e:
        print(f"❌ Error verifying CVV trigger: {e}")

if __name__ == '__main__':
    verify_trigger()
