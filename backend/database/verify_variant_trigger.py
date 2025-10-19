"""
Verify Variant Quantity Trigger
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection


def verify_trigger():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TRIGGERS WHERE `Trigger` = 'check_variant_quantity'")
        trigger = cursor.fetchone()
        if trigger:
            print("✅ Variant trigger verified!")
            print(f"   Name: {trigger[0]}")
            print(f"   Event: {trigger[1]}")
            print(f"   Table: {trigger[2]}")
            print(f"   Timing: {trigger[4]}")
        else:
            print("❌ Variant trigger not found")
    except Exception as e:
        print(f"❌ Error verifying trigger: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    verify_trigger()
