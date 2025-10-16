"""
Verify GetOrderSummary Stored Procedure
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import text
from app.database import engine


def verify_procedure():
    try:
        conn = engine.connect()
        
        # Check if procedure exists
        result = conn.execute(text("""
            SELECT ROUTINE_NAME, ROUTINE_TYPE 
            FROM information_schema.ROUTINES 
            WHERE ROUTINE_SCHEMA = DATABASE() 
            AND ROUTINE_NAME = 'GetOrderSummary'
        """))
        
        procedure = result.fetchone()
        
        if procedure:
            print("✅ GetOrderSummary stored procedure verified!")
            print(f"   Name: {procedure[0]}")
            print(f"   Type: {procedure[1]}")
            print("\n   Parameters:")
            print("   - IN p_user_id INT")
            print("\n   Returns:")
            print("   - order_id, order_date, total_amount")
            print("   - quantity, price, product_name")
            print("   - variant_name, delivery_status")
        else:
            print("❌ GetOrderSummary procedure not found")
            print("   Run: python database/apply_order_summary_procedure.py")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verifying procedure: {e}")


if __name__ == '__main__':
    verify_procedure()
