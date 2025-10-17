import requests

try:
    r = requests.get('http://127.0.0.1:8020/categories/')
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Categories found: {len(data)}")
        if len(data) > 0:
            print(f"First category: {data[0]}")
    else:
        print(f"Error: {r.text}")
except Exception as e:
    print(f"Connection error: {e}")
