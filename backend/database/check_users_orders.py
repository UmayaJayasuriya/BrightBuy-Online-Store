"""
Check which users have orders in the database
"""

import sys
sys.path.insert(0, '.')
from app.database import get_connection

def check_data():
    """Check users and orders"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check users
        print("👤 Users in database:")
        print("-" * 80)
        cursor.execute("SELECT user_id, user_name, email FROM User LIMIT 10")
        user_rows = cursor.fetchall()
        
        if user_rows:
            for user in user_rows:
                print(f"   ID: {user[0]} | Username: {user[1]} | Email: {user[2]}")
        else:
            print("   No users found")
        
        # Check orders
        print("\n📦 Orders in database:")
        print("-" * 80)
        cursor.execute("""
            SELECT o.order_id, o.user_id, u.user_name, o.order_date, o.total_amount 
            FROM `Order` o 
            JOIN User u ON o.user_id = u.user_id 
            ORDER BY o.order_date DESC 
            LIMIT 10
        """)
        order_rows = cursor.fetchall()
        
        if order_rows:
            for order in order_rows:
                print(f"   Order #{order[0]} | User: {order[2]} (ID: {order[1]}) | Date: {order[3]} | Total: ${order[4]:.2f}")
                
            # Test procedure with first user who has orders
            test_user_id = order_rows[0][1]
            print(f"\n🧪 Testing GetOrderSummary with user_id={test_user_id}...")
            print("-" * 80)
            
            cursor.execute("CALL GetOrderSummary(%s)", (test_user_id,))
            proc_rows = cursor.fetchall()
            
            print(f"✅ Procedure returned {len(proc_rows)} rows")
            
            if proc_rows:
                print("\nSample row:")
                row = proc_rows[0]
                print(f"   Order ID: {row[0]}")
                print(f"   Date: {row[1]}")
                print(f"   Total: ${row[2]:.2f}")
                print(f"   Product: {row[5]}")
                print(f"   Variant: {row[6]}")
                print(f"   Delivery Status: {row[7]}")
                
        else:
            print("   No orders found in database")
        
        print("\n✅ Check complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    check_data()
