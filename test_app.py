"""
Quick test script to verify the application is working.
Tests basic endpoints and authentication.
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_landing_page():
    """Test the landing page."""
    print("Testing landing page...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✓ Landing page works!")
        return True
    else:
        print(f"✗ Landing page failed: {response.status_code}")
        return False

def test_login_page():
    """Test the login page."""
    print("\nTesting login page...")
    response = requests.get(f"{BASE_URL}/login")
    if response.status_code == 200:
        print("✓ Login page works!")
        return True
    else:
        print(f"✗ Login page failed: {response.status_code}")
        return False

def test_api_login():
    """Test API login."""
    print("\nTesting API login...")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    login_data = {
        "email": "admin@versatiles.com",
        "password": "Admin123!"
    }
    
    response = session.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("✓ API login works!")
        data = response.json()
        print(f"  Logged in as: {data.get('user', {}).get('email')}")
        print(f"  Role: {data.get('user', {}).get('role_name')}")
        return True, session
    else:
        print(f"✗ API login failed: {response.status_code}")
        print(f"  Response: {response.text}")
        return False, None

def test_dashboard_access(session):
    """Test dashboard access (requires login)."""
    print("\nTesting dashboard access...")
    
    if not session:
        print("✗ No session available")
        return False
    
    response = session.get(f"{BASE_URL}/dashboard")
    if response.status_code == 200:
        print("✓ Dashboard access works!")
        return True
    else:
        print(f"✗ Dashboard access failed: {response.status_code}")
        return False

def test_api_users(session):
    """Test users API (admin only)."""
    print("\nTesting users API...")
    
    if not session:
        print("✗ No session available")
        return False
    
    response = session.get(f"{BASE_URL}/api/users")
    if response.status_code == 200:
        print("✓ Users API works!")
        data = response.json()
        print(f"  Total users: {data.get('total', 0)}")
        return True
    else:
        print(f"✗ Users API failed: {response.status_code}")
        return False

def test_api_orders(session):
    """Test orders API."""
    print("\nTesting orders API...")
    
    if not session:
        print("✗ No session available")
        return False
    
    response = session.get(f"{BASE_URL}/api/orders")
    if response.status_code == 200:
        print("✓ Orders API works!")
        data = response.json()
        print(f"  Total orders: {data.get('total', 0)}")
        return True
    else:
        print(f"✗ Orders API failed: {response.status_code}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("VersatilesPrint Application Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test landing page
    results.append(("Landing Page", test_landing_page()))
    
    # Test login page
    results.append(("Login Page", test_login_page()))
    
    # Test API login
    login_success, session = test_api_login()
    results.append(("API Login", login_success))
    
    if login_success and session:
        # Test authenticated endpoints
        results.append(("Dashboard Access", test_dashboard_access(session)))
        results.append(("Users API", test_api_users(session)))
        results.append(("Orders API", test_api_orders(session)))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Application is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to the application.")
        print("Make sure the Flask server is running on http://localhost:5000")
        print("Run: python run.py")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
