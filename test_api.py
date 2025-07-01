import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_purposes():
    """Test purposes endpoints"""
    print("Testing purposes endpoints...")
    
    # Get all purposes
    response = requests.get(f"{BASE_URL}/purposes")
    print(f"Get all purposes - Status: {response.status_code}")
    purposes = response.json()
    print(f"Found {len(purposes)} purposes")
    
    if purposes:
        # Get specific purpose
        purpose_id = purposes[0]['id']
        response = requests.get(f"{BASE_URL}/purposes/{purpose_id}")
        print(f"Get specific purpose - Status: {response.status_code}")
        print(f"Purpose: {response.json()}")
    
    print()

def test_consent_operations():
    """Test consent operations"""
    print("Testing consent operations...")
    
    user_id = "test_user_123"
    
    # Test bulk consent update
    bulk_data = {
        "user_id": user_id,
        "consents": [
            {"purpose_id": 1, "status": True},
            {"purpose_id": 2, "status": False},
            {"purpose_id": 3, "status": True}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/consent/bulk", json=bulk_data)
    print(f"Bulk consent update - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test getting user consents
    response = requests.get(f"{BASE_URL}/consent?user_id={user_id}")
    print(f"Get user consents - Status: {response.status_code}")
    consents = response.json()
    print(f"Found {len(consents)} consent records")
    
    # Test individual consent update
    if consents:
        consent_id = consents[0]['id']
        response = requests.get(f"{BASE_URL}/consent/{consent_id}")
        print(f"Get specific consent - Status: {response.status_code}")
        print(f"Consent: {response.json()}")
    
    print()

def test_consent_check():
    """Test consent check endpoint"""
    print("Testing consent check...")
    
    check_data = {
        "user_id": "test_user_123",
        "purpose_ids": [1, 2, 3, 4]
    }
    
    response = requests.post(f"{BASE_URL}/consent/check", json=check_data)
    print(f"Consent check - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_user_history():
    """Test user consent history"""
    print("Testing user consent history...")
    
    user_id = "test_user_123"
    response = requests.get(f"{BASE_URL}/consent/user/{user_id}/history")
    print(f"User history - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_statistics():
    """Test statistics endpoint"""
    print("Testing statistics...")
    
    response = requests.get(f"{BASE_URL}/consent/stats")
    print(f"Statistics - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test invalid purpose ID
    response = requests.get(f"{BASE_URL}/purposes/999")
    print(f"Invalid purpose ID - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test missing user_id
    response = requests.get(f"{BASE_URL}/consent")
    print(f"Missing user_id - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test invalid consent data
    invalid_data = {"user_id": "test", "purpose_id": 999, "status": True}
    response = requests.post(f"{BASE_URL}/consent", json=invalid_data)
    print(f"Invalid consent data - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print()

def main():
    """Run all tests"""
    print("Starting API tests...")
    print("=" * 50)
    
    try:
        test_health_check()
        test_purposes()
        test_consent_operations()
        test_consent_check()
        test_user_history()
        test_statistics()
        test_error_handling()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 