"""
Test Analytics Endpoints
Quick script to test all the new stored procedure endpoints
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8020/analytics"

def print_response(title, response):
    """Pretty print API response"""
    print("\n" + "=" * 80)
    print(f"TEST: {title}")
    print("=" * 80)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS")
        data = response.json()
        print(json.dumps(data, indent=2, default=str))
    else:
        print("❌ FAILED")
        print(response.text)
    print("=" * 80)


def test_all_endpoints():
    """Test all analytics endpoints"""
    
    print("\n" + "🚀" * 40)
    print("BrightBuy Analytics Endpoints - Integration Test")
    print("🚀" * 40)
    
    # Test 1: Get Cart Details
    try:
        response = requests.get(f"{BASE_URL}/cart/1")
        print_response("GET Cart Details (user_id=1)", response)
    except Exception as e:
        print(f"\n❌ Error testing cart endpoint: {e}")
    
    # Test 2: Get Products by Category
    try:
        response = requests.get(f"{BASE_URL}/products/category", params={"category_id": 1})
        print_response("GET Products by Category (category_id=1)", response)
    except Exception as e:
        print(f"\n❌ Error testing products endpoint: {e}")
    
    # Test 3: Get All Products
    try:
        response = requests.get(f"{BASE_URL}/products/category")
        print_response("GET All Products (no category filter)", response)
    except Exception as e:
        print(f"\n❌ Error testing all products endpoint: {e}")
    
    # Test 4: Get Low Stock Variants
    try:
        response = requests.get(f"{BASE_URL}/inventory/low-stock", params={"threshold": 50})
        print_response("GET Low Stock Variants (threshold=50)", response)
    except Exception as e:
        print(f"\n❌ Error testing low stock endpoint: {e}")
    
    # Test 5: Get Sales Report
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        response = requests.get(
            f"{BASE_URL}/sales/report",
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )
        print_response("GET Sales Report (last 30 days)", response)
    except Exception as e:
        print(f"\n❌ Error testing sales report endpoint: {e}")
    
    # Test 6: Get Top Selling Products
    try:
        response = requests.get(
            f"{BASE_URL}/products/top-selling",
            params={"limit": 5, "days": 30}
        )
        print_response("GET Top Selling Products (top 5, last 30 days)", response)
    except Exception as e:
        print(f"\n❌ Error testing top selling endpoint: {e}")
    
    # Test 7: Get Customer Order History
    try:
        response = requests.get(f"{BASE_URL}/customers/1/order-history")
        print_response("GET Customer Order History (user_id=1)", response)
    except Exception as e:
        print(f"\n❌ Error testing order history endpoint: {e}")
    
    # Test 8: Update Order Status (if you have an order)
    print("\n" + "=" * 80)
    print("TEST: PUT Update Order Status (order_id=1)")
    print("=" * 80)
    print("⚠️  SKIPPED - This modifies data. To test manually:")
    print("   curl -X PUT 'http://127.0.0.1:8020/analytics/orders/1/status' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"status\": \"Shipped\"}'")
    print("=" * 80)
    
    # Summary
    print("\n" + "🎉" * 40)
    print("Testing Complete!")
    print("🎉" * 40)
    print("\n📊 Summary:")
    print("   ✅ 7 GET endpoints tested")
    print("   ⚠️  1 PUT endpoint skipped (modifies data)")
    print("\n💡 Next Steps:")
    print("   1. Check the responses above for any errors")
    print("   2. Visit http://127.0.0.1:8020/docs for interactive API docs")
    print("   3. Integrate these endpoints into your frontend")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n⚠️  PREREQUISITES:")
    print("   1. FastAPI server must be running on port 8020")
    print("   2. Stored procedures must be installed")
    print("   3. Database must have some test data")
    print("\nStarting tests in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        test_all_endpoints()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("   Make sure FastAPI is running:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --host 127.0.0.1 --port 8020 --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
