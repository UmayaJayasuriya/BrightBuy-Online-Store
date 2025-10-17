import requests

try:
    # Test products endpoint
    r = requests.get('http://127.0.0.1:8020/products/')
    print(f"Products Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Total products found: {len(data)}")
        if len(data) > 0:
            print(f"First product: {data[0].get('product_name', 'N/A')}")
    else:
        print(f"Error: {r.text}")
    
    # Test products by category
    print("\n--- Testing by category ---")
    r2 = requests.get('http://127.0.0.1:8020/products/?category_name=Smartphones')
    print(f"Smartphones Status: {r2.status_code}")
    if r2.status_code == 200:
        data2 = r2.json()
        print(f"Smartphones found: {len(data2)}")
        
except Exception as e:
    print(f"Connection error: {e}")
