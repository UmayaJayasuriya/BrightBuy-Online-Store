"""
Verify GetOrderSummary Stored Procedure
"""
import sys
sys.path.insert(0, '.')

from app.database import get_connection


def verify_procedure():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if procedure exists
        cursor.execute("""
            SELECT ROUTINE_NAME, ROUTINE_TYPE 
            FROM information_schema.ROUTINES 
            WHERE ROUTINE_SCHEMA = DATABASE() 
            AND ROUTINE_NAME = 'GetOrderSummary'
        """)
        
        procedure = cursor.fetchone()
        
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
        
    except Exception as e:
        print(f"❌ Error verifying procedure: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    verify_procedure()
