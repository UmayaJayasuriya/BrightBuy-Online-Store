"""
Debug GetOrderSummary Stored Procedure
Check what data is actually being returned
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/brightbuy')

def debug_procedure():
    """Debug the GetOrderSummary procedure"""
    try:
        engine = create_engine(DATABASE_URL)
        
        test_user_id = 10
        
        print(f"🔍 Calling GetOrderSummary for user_id={test_user_id}")
        print("-" * 80)
        
        with engine.connect() as conn:
            # Call the stored procedure
            result = conn.execute(
                text("CALL GetOrderSummary(:p_user_id)"),
                {"p_user_id": test_user_id}
            )
            
            rows = result.fetchall()
            
            print(f"📊 Total rows returned: {len(rows)}")
            print("-" * 80)
            
            # Show first 10 rows
            print("\nFirst 10 rows:")
            for i, row in enumerate(rows[:10], 1):
                print(f"\nRow {i}:")
                print(f"  Order ID: {row[0]}")
                print(f"  Order Date: {row[1]}")
                print(f"  Total Amount: {row[2]}")
                print(f"  Quantity: {row[3]}")
                print(f"  Price: {row[4]}")
                print(f"  Product: {row[5]}")
                print(f"  Variant: {row[6]}")
                print(f"  Status: {row[7] if len(row) > 7 else 'N/A'}")
            
            # Count unique order_ids
            order_ids = set(row[0] for row in rows)
            print(f"\n📦 Unique order IDs: {order_ids}")
            print(f"📦 Number of unique orders: {len(order_ids)}")
            
            # Count items per order
            print("\n📊 Items per order:")
            from collections import defaultdict
            order_items = defaultdict(list)
            for row in rows:
                order_items[row[0]].append((row[5], row[6]))  # product, variant
            
            for order_id, items in order_items.items():
                print(f"  Order #{order_id}: {len(items)} items")
                # Show unique items
                unique_items = set(items)
                print(f"    Unique items: {len(unique_items)}")
                if len(items) != len(unique_items):
                    print(f"    ⚠️ DUPLICATES DETECTED!")
        
        print("\n✅ Debug complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_procedure()
