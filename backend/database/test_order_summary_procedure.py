"""
Test GetOrderSummary Stored Procedure
This script calls the stored procedure and displays results
"""

import sys
sys.path.insert(0, '.')
from app.database import get_connection

def test_procedure():
    """Test the GetOrderSummary procedure"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get a user ID to test (you can change this)
        test_user_id = 1
        
        print(f"🔍 Testing GetOrderSummary procedure for user_id={test_user_id}...")
        print("-" * 80)
        
        # Call the stored procedure
        cursor.execute("CALL GetOrderSummary(%s)", (test_user_id,))
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        if not rows:
            print(f"ℹ️  No orders found for user_id={test_user_id}")
            print("\nTo test with a different user, modify test_user_id in the script.")
            return
        
        print(f"✅ Found {len(rows)} order items for user_id={test_user_id}\n")
        
        # Display results
        print("Order Details:")
        print("-" * 80)
        
        current_order = None
        order_count = 0
        
        for row in rows:
            order_id = row[0]
            order_date = row[1]
            total_amount = row[2]
            quantity = row[3]
            price = row[4]
            product_name = row[5]
            variant_name = row[6]
            delivery_status = row[7]
            
            # New order
            if order_id != current_order:
                if current_order is not None:
                    print("-" * 80)
                
                order_count += 1
                current_order = order_id
                
                print(f"\n📦 Order #{order_id}")
                print(f"   Date: {order_date}")
                print(f"   Total: ${total_amount:.2f}")
                print(f"   Status: {delivery_status}")
                print(f"\n   Items:")
            
            # Order item
            item_total = quantity * price
            print(f"   - {product_name} ({variant_name})")
            print(f"     Qty: {quantity} × ${price:.2f} = ${item_total:.2f}")
        
        print("\n" + "=" * 80)
        print(f"📊 Summary: {order_count} order(s) with {len(rows)} total item(s)")
        print("=" * 80)
        
        # Verify JOIN is working
        print("\n🔍 Checking for NULL product/variant names (indicates JOIN issue)...")
        null_products = [r for r in rows if r[5] is None or r[6] is None]
        
        if null_products:
            print(f"⚠️  WARNING: Found {len(null_products)} items with NULL product/variant names")
            print("   This indicates the JOIN condition may be incorrect.")
            print("   The procedure needs to be updated with the correct JOIN:")
            print("   LEFT JOIN variant v ON oi.variant_id = v.variant_id")
        else:
            print("✅ All items have product and variant names - JOINs are working correctly!")
        
        print("\n✅ Procedure test complete!")
        
    except Exception as e:
        print(f"\n❌ Error testing procedure: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    test_procedure()
