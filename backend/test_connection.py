import requests

def test_backend():
    try:
        # Test basic connection
        response = requests.get('http://127.0.0.1:8020/ping-db')
        print(f"Database Connection Test: {response.json()}")
        
        # Test CORS
        headers = {
            'Origin': 'http://localhost:3000'
        }
        response = requests.options('http://127.0.0.1:8020/auth/login', headers=headers)
        print(f"CORS Test Status: {response.status_code}")
        print(f"CORS Headers: {response.headers}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Make sure it's running on port 8020")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_backend()