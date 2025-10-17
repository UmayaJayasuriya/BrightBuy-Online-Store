import requests

BASE_URL = "http://127.0.0.1:8020"

print("Testing Bestsellers Endpoint")
print("=" * 60)

# Test the bestsellers endpoint
response = requests.get(f"{BASE_URL}/products/bestsellers/")

if response.status_code == 200:
    bestsellers = response.json()
    print(f"\n✅ Success! Found {len(bestsellers)} bestselling products\n")
    
    if bestsellers:
        print("Top Bestselling Products:")
        print("-" * 60)
        for i, product in enumerate(bestsellers, 1):
            print(f"{i}. {product['product_name']}")
            print(f"   Category: {product['category']['category_name'] if product.get('category') else 'N/A'}")
            print(f"   Product ID: {product['product_id']}")
            print()
    else:
        print("⚠️  No bestsellers found. This means no orders have been placed yet.")
        print("   Products will appear here once customers start placing orders.")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"   {response.text}")

print("=" * 60)
