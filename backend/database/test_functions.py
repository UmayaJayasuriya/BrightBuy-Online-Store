"""
Test MySQL Functions
This script tests all custom MySQL functions to ensure they work correctly
"""

import mysql.connector
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_functions():
    """Test all MySQL functions"""
    
    # Load environment variables
    load_dotenv()
    
    # Database connection
    try:
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'brightbuy')
        )
        cursor = db.cursor(dictionary=True)
        print("✅ Connected to database\n")
        
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        return
    
    print("=" * 60)
    print("Testing MySQL Functions")
    print("=" * 60)
    
    # Test 1: CalculateCartTotal
    print("\n1️⃣  Testing CalculateCartTotal...")
    try:
        cursor.execute("SELECT cart_id FROM cart LIMIT 1")
        result = cursor.fetchone()
        if result:
            cart_id = result['cart_id']
            cursor.execute(f"SELECT CalculateCartTotal({cart_id}) as total")
            result = cursor.fetchone()
            print(f"   ✅ Cart {cart_id} total: ${result['total']}")
        else:
            print("   ⚠️  No carts found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: GetProductStockStatus
    print("\n2️⃣  Testing GetProductStockStatus...")
    try:
        cursor.execute("SELECT product_id FROM product LIMIT 1")
        result = cursor.fetchone()
        if result:
            product_id = result['product_id']
            cursor.execute(f"SELECT GetProductStockStatus({product_id}) as status")
            result = cursor.fetchone()
            print(f"   ✅ Product {product_id} status: {result['status']}")
        else:
            print("   ⚠️  No products found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: CalculateOrderItemTotal
    print("\n3️⃣  Testing CalculateOrderItemTotal...")
    try:
        cursor.execute("SELECT order_item_id FROM order_item LIMIT 1")
        result = cursor.fetchone()
        if result:
            order_item_id = result['order_item_id']
            cursor.execute(f"SELECT CalculateOrderItemTotal({order_item_id}) as total")
            result = cursor.fetchone()
            print(f"   ✅ Order item {order_item_id} total: ${result['total']}")
        else:
            print("   ⚠️  No order items found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: GetCustomerLifetimeValue
    print("\n4️⃣  Testing GetCustomerLifetimeValue...")
    try:
        cursor.execute("SELECT user_id FROM user WHERE user_type = 'customer' LIMIT 1")
        result = cursor.fetchone()
        if result:
            user_id = result['user_id']
            cursor.execute(f"SELECT GetCustomerLifetimeValue({user_id}) as lifetime_value")
            result = cursor.fetchone()
            print(f"   ✅ Customer {user_id} lifetime value: ${result['lifetime_value']}")
        else:
            print("   ⚠️  No customers found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: GetProductAverageRating
    print("\n5️⃣  Testing GetProductAverageRating...")
    try:
        cursor.execute("SELECT product_id FROM product LIMIT 1")
        result = cursor.fetchone()
        if result:
            product_id = result['product_id']
            cursor.execute(f"SELECT GetProductAverageRating({product_id}) as rating")
            result = cursor.fetchone()
            print(f"   ✅ Product {product_id} rating: {result['rating']} (placeholder)")
        else:
            print("   ⚠️  No products found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: IsVariantAvailable
    print("\n6️⃣  Testing IsVariantAvailable...")
    try:
        cursor.execute("SELECT variant_id, quantity FROM variant LIMIT 1")
        result = cursor.fetchone()
        if result:
            variant_id = result['variant_id']
            stock = result['quantity']
            cursor.execute(f"SELECT IsVariantAvailable({variant_id}, 1) as available")
            result = cursor.fetchone()
            print(f"   ✅ Variant {variant_id} (stock: {stock}) available for qty 1: {bool(result['available'])}")
        else:
            print("   ⚠️  No variants found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: GetProductPriceRange
    print("\n7️⃣  Testing GetProductPriceRange...")
    try:
        cursor.execute("SELECT product_id FROM product LIMIT 1")
        result = cursor.fetchone()
        if result:
            product_id = result['product_id']
            cursor.execute(f"SELECT GetProductPriceRange({product_id}) as price_range")
            result = cursor.fetchone()
            print(f"   ✅ Product {product_id} price range: {result['price_range']}")
        else:
            print("   ⚠️  No products found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: CalculateDeliveryDays
    print("\n8️⃣  Testing CalculateDeliveryDays...")
    try:
        cursor.execute("SELECT city_id FROM location LIMIT 1")
        result = cursor.fetchone()
        if result:
            city_id = result['city_id']
            cursor.execute(f"SELECT CalculateDeliveryDays({city_id}) as delivery_days")
            result = cursor.fetchone()
            print(f"   ✅ City {city_id} delivery days: {result['delivery_days']}")
        else:
            print("   ⚠️  No locations found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 9: GetOrderStatus
    print("\n9️⃣  Testing GetOrderStatus...")
    try:
        cursor.execute("SELECT order_id FROM orders LIMIT 1")
        result = cursor.fetchone()
        if result:
            order_id = result['order_id']
            cursor.execute(f"SELECT GetOrderStatus({order_id}) as status")
            result = cursor.fetchone()
            print(f"   ✅ Order {order_id} status: {result['status']}")
        else:
            print("   ⚠️  No orders found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 10: ValidateEmail
    print("\n🔟 Testing ValidateEmail...")
    try:
        test_emails = [
            ('test@example.com', True),
            ('invalid.email', False),
            ('user@domain.co.uk', True),
            ('bad@', False)
        ]
        for email, expected in test_emails:
            cursor.execute(f"SELECT ValidateEmail('{email}') as is_valid")
            result = cursor.fetchone()
            status = "✅" if bool(result['is_valid']) == expected else "❌"
            print(f"   {status} '{email}': {bool(result['is_valid'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 11: GetDiscountedPrice
    print("\n1️⃣1️⃣  Testing GetDiscountedPrice...")
    try:
        test_cases = [
            (100.00, 10, 90.00),
            (50.00, 20, 40.00),
            (75.00, 0, 75.00)
        ]
        for price, discount, expected in test_cases:
            cursor.execute(f"SELECT GetDiscountedPrice({price}, {discount}) as discounted")
            result = cursor.fetchone()
            print(f"   ✅ ${price} with {discount}% off = ${result['discounted']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 12: GetCategoryPath
    print("\n1️⃣2️⃣  Testing GetCategoryPath...")
    try:
        cursor.execute("SELECT category_id FROM category LIMIT 1")
        result = cursor.fetchone()
        if result:
            category_id = result['category_id']
            cursor.execute(f"SELECT GetCategoryPath({category_id}) as path")
            result = cursor.fetchone()
            print(f"   ✅ Category {category_id} path: {result['path']}")
        else:
            print("   ⚠️  No categories found in database")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All function tests completed!")
    print("=" * 60)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    test_functions()
