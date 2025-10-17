import requests

# Test the delete variant endpoint
BASE_URL = "http://127.0.0.1:8020"

# First, get a list of variants to see what we have
print("Fetching product with variants...")
response = requests.get(f"{BASE_URL}/products/1/variants/")
if response.status_code == 200:
    product = response.json()
    print(f"\nProduct: {product['product_name']}")
    print(f"Number of variants: {len(product['variants'])}")
    
    if product['variants']:
        print("\nVariants:")
        for v in product['variants']:
            print(f"  - ID: {v['variant_id']}, Name: {v['variant_name']}, SKU: {v['SKU']}")
            
            # Check if variant is in any orders
            check_response = requests.get(f"{BASE_URL}/admin/orders")
            if check_response.status_code == 200:
                orders = check_response.json()
                print(f"    Total orders in system: {len(orders)}")
else:
    print(f"Error: {response.status_code} - {response.text}")

print("\n" + "="*60)
print("To test deletion, you would need:")
print("1. Admin authentication token")
print("2. A variant_id that is NOT in any orders")
print("3. Use: DELETE /admin/variants/{variant_id}")
print("="*60)
