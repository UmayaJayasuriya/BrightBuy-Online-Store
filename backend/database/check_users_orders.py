"""
Check which users have orders in the database
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/brightbuy')

def check_data():
    """Check users and orders"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Check users
            print("👤 Users in database:")
            print("-" * 80)
            users = conn.execute(text("SELECT user_id, user_name, email FROM User LIMIT 10"))
            user_rows = users.fetchall()
            
            if user_rows:
                for user in user_rows:
                    print(f"   ID: {user[0]} | Username: {user[1]} | Email: {user[2]}")
            else:
                print("   No users found")
            
            # Check orders
            print("\n📦 Orders in database:")
            print("-" * 80)
            orders = conn.execute(text("""
                SELECT o.order_id, o.user_id, u.user_name, o.order_date, o.total_amount 
                FROM `Order` o 
                JOIN User u ON o.user_id = u.user_id 
                ORDER BY o.order_date DESC 
                LIMIT 10
            """))
            order_rows = orders.fetchall()
            
            if order_rows:
                for order in order_rows:
                    print(f"   Order #{order[0]} | User: {order[2]} (ID: {order[1]}) | Date: {order[3]} | Total: ${order[4]:.2f}")
                    
                # Test procedure with first user who has orders
                test_user_id = order_rows[0][1]
                print(f"\n🧪 Testing GetOrderSummary with user_id={test_user_id}...")
                print("-" * 80)
                
                result = conn.execute(
                    text("CALL GetOrderSummary(:p_user_id)"),
                    {"p_user_id": test_user_id}
                )
                proc_rows = result.fetchall()
                
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

if __name__ == "__main__":
    check_data()
