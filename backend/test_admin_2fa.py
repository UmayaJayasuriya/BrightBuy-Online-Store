"""
Test script for Admin 2FA functionality
Run this after setting up the database table and email configuration
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_admin_2fa_flow():
    """Test the complete admin 2FA flow"""
    
    print("=" * 60)
    print("Testing Admin 2FA Flow")
    print("=" * 60)
    
    # Test 1: Admin login (should trigger 2FA)
    print("\n1. Testing admin login (should send verification code)...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "identifier": "admin",  # Replace with your admin username/email
            "password": "admin123"  # Replace with your admin password
        }
    )
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        print(f"   ✓ Status: {login_response.status_code}")
        print(f"   ✓ Message: {login_data['message']}")
        print(f"   ✓ Requires 2FA: {login_data['requires_2fa']}")
        print(f"   ✓ User ID: {login_data['user_id']}")
        print(f"   ✓ Email: {login_data['email']}")
        
        if login_data['requires_2fa']:
            print("\n   📧 Check your email for the verification code!")
            
            # Test 2: Verify 2FA code
            print("\n2. Testing 2FA verification...")
            code = input("   Enter the 6-digit code from your email: ")
            
            verify_response = requests.post(
                f"{BASE_URL}/auth/verify-2fa",
                json={
                    "user_id": login_data['user_id'],
                    "verification_code": code
                }
            )
            
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                print(f"   ✓ Status: {verify_response.status_code}")
                print(f"   ✓ Message: {verify_data['message']}")
                print(f"   ✓ Access Token: {verify_data['access_token'][:50]}...")
                print(f"   ✓ Token Type: {verify_data['token_type']}")
                print("\n   ✅ Admin 2FA flow completed successfully!")
            else:
                print(f"   ✗ Verification failed: {verify_response.status_code}")
                print(f"   ✗ Error: {verify_response.json()}")
        else:
            print("   ✗ User is not an admin or 2FA not triggered")
    else:
        print(f"   ✗ Login failed: {login_response.status_code}")
        print(f"   ✗ Error: {login_response.json()}")

def test_regular_user_login():
    """Test that regular users don't require 2FA"""
    
    print("\n" + "=" * 60)
    print("Testing Regular User Login (No 2FA)")
    print("=" * 60)
    
    print("\n1. Testing regular user login (should NOT require 2FA)...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "identifier": "customer",  # Replace with a customer username/email
            "password": "customer123"  # Replace with customer password
        }
    )
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        print(f"   ✓ Status: {login_response.status_code}")
        print(f"   ✓ Message: {login_data['message']}")
        print(f"   ✓ Requires 2FA: {login_data['requires_2fa']}")
        print(f"   ✓ User Type: {login_data['user_type']}")
        
        if not login_data['requires_2fa'] and login_data.get('access_token'):
            print(f"   ✓ Access Token: {login_data['access_token'][:50]}...")
            print("\n   ✅ Regular user login works without 2FA!")
        else:
            print("   ⚠️ Warning: Regular user triggered 2FA")
    else:
        print(f"   ✗ Login failed: {login_response.status_code}")
        print(f"   ✗ Error: {login_response.json()}")

def test_invalid_code():
    """Test invalid verification code handling"""
    
    print("\n" + "=" * 60)
    print("Testing Invalid Code Handling")
    print("=" * 60)
    
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "identifier": "admin",
            "password": "admin123"
        }
    )
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        user_id = login_data['user_id']
        
        print("\n2. Testing invalid verification code...")
        verify_response = requests.post(
            f"{BASE_URL}/auth/verify-2fa",
            json={
                "user_id": user_id,
                "verification_code": "000000"  # Invalid code
            }
        )
        
        if verify_response.status_code == 401:
            print(f"   ✓ Status: {verify_response.status_code}")
            print(f"   ✓ Error message: {verify_response.json()['detail']}")
            print("\n   ✅ Invalid code properly rejected!")
        else:
            print(f"   ✗ Unexpected response: {verify_response.status_code}")

def test_expired_code():
    """Test expired code handling"""
    
    print("\n" + "=" * 60)
    print("Testing Expired Code Handling")
    print("=" * 60)
    
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "identifier": "admin",
            "password": "admin123"
        }
    )
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        print("   ✓ Login successful, code sent")
        print("\n2. Waiting 11 minutes for code to expire...")
        print("   (Skipping this test - would take too long)")
        print("   💡 To test manually: Wait 11 minutes and try to use the code")

if __name__ == "__main__":
    print("\n🔐 Admin 2FA Test Suite")
    print("=" * 60)
    print("Make sure:")
    print("1. Backend server is running (python -m uvicorn app.main:app --reload)")
    print("2. Database table is created (python database/create_admin_2fa_table.py)")
    print("3. Email configuration is set in .env file")
    print("4. You have at least one admin user in the database")
    print("=" * 60)
    
    proceed = input("\nReady to proceed? (y/n): ")
    
    if proceed.lower() == 'y':
        try:
            # Test admin 2FA flow
            test_admin_2fa_flow()
            
            # Test regular user login
            test_regular = input("\n\nTest regular user login? (y/n): ")
            if test_regular.lower() == 'y':
                test_regular_user_login()
            
            # Test invalid code
            test_invalid = input("\n\nTest invalid code handling? (y/n): ")
            if test_invalid.lower() == 'y':
                test_invalid_code()
            
            print("\n" + "=" * 60)
            print("✅ Testing Complete!")
            print("=" * 60)
            
        except requests.exceptions.ConnectionError:
            print("\n❌ Error: Could not connect to the server.")
            print("Make sure the backend is running on http://localhost:8000")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    else:
        print("\nTest cancelled.")
