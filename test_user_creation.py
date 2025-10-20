"""
Test script to verify user creation API
"""
import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:5000"
LOGIN_EMAIL = "admin@versatiles.com"
LOGIN_PASSWORD = "Admin123!"

def test_user_creation():
    """Test the user creation flow"""
    
    print("=" * 60)
    print("Testing User Creation API")
    print("=" * 60)
    
    # Step 1: Login to get session
    print("\n1. Logging in as admin...")
    session = requests.Session()
    
    login_response = session.post(
        f"{BASE_URL}/login",
        data={
            "email": LOGIN_EMAIL,
            "password": LOGIN_PASSWORD
        },
        allow_redirects=False
    )
    
    if login_response.status_code not in [200, 302]:
        print(f"   ❌ Login failed: {login_response.status_code}")
        return
    
    print("   ✅ Login successful")
    
    # Step 2: Test user creation with valid data
    print("\n2. Testing user creation with valid data...")
    
    test_user_data = {
        "email": "test@example.com",
        "password": "TestPass123",
        "full_name": "Test User",
        "role": "Client",
        "is_active": True
    }
    
    print(f"   Request data: {json.dumps(test_user_data, indent=2)}")
    
    create_response = session.post(
        f"{BASE_URL}/api/users",
        json=test_user_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n   Response status: {create_response.status_code}")
    print(f"   Response headers: {dict(create_response.headers)}")
    
    try:
        response_data = create_response.json()
        print(f"   Response body: {json.dumps(response_data, indent=2)}")
        
        if create_response.status_code == 201:
            print("\n   ✅ User created successfully!")
        elif create_response.status_code == 400:
            print(f"\n   ❌ Validation error: {response_data.get('error', {}).get('message')}")
        else:
            print(f"\n   ❌ Unexpected status code: {create_response.status_code}")
            
    except json.JSONDecodeError:
        print(f"   ❌ Invalid JSON response: {create_response.text}")
    
    # Step 3: Test with missing password
    print("\n3. Testing user creation with missing password...")
    
    invalid_data = {
        "email": "test2@example.com",
        "full_name": "Test User 2",
        "role": "Client"
        # Missing password
    }
    
    create_response2 = session.post(
        f"{BASE_URL}/api/users",
        json=invalid_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"   Response status: {create_response2.status_code}")
    try:
        response_data2 = create_response2.json()
        print(f"   Response: {json.dumps(response_data2, indent=2)}")
        
        if create_response2.status_code == 400:
            print("   ✅ Correctly rejected missing password")
        else:
            print("   ❌ Should have rejected missing password")
    except json.JSONDecodeError:
        print(f"   ❌ Invalid JSON response: {create_response2.text}")
    
    # Step 4: Test with weak password
    print("\n4. Testing user creation with weak password...")
    
    weak_password_data = {
        "email": "test3@example.com",
        "password": "weak",  # Too short, no uppercase, no digit
        "full_name": "Test User 3",
        "role": "Client"
    }
    
    create_response3 = session.post(
        f"{BASE_URL}/api/users",
        json=weak_password_data,
        headers={"Content-Type": "application/json"}
    }
    
    print(f"   Response status: {create_response3.status_code}")
    try:
        response_data3 = create_response3.json()
        print(f"   Response: {json.dumps(response_data3, indent=2)}")
        
        if create_response3.status_code == 400:
            print("   ✅ Correctly rejected weak password")
        else:
            print("   ❌ Should have rejected weak password")
    except json.JSONDecodeError:
        print(f"   ❌ Invalid JSON response: {create_response3.text}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_user_creation()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
