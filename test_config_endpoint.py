#!/usr/bin/env python3
"""
Quick test to verify /config endpoint returns valid JSON
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_config_get():
    """Test GET /config"""
    print("Testing GET /config...")
    try:
        response = requests.get(f"{BASE_URL}/config")
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Response: {response.text}")
        
        data = response.json()
        print(f"✅ Valid JSON received: {data}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config_post():
    """Test POST /config"""
    print("\nTesting POST /config...")
    try:
        payload = {"host": "192.168.0.104", "port": "4433"}
        response = requests.post(
            f"{BASE_URL}/config",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Response: {response.text}")
        
        data = response.json()
        print(f"✅ Valid JSON received: {data}")
        
        if data.get('status') == 'success':
            print(f"✅ Configuration updated successfully")
            return True
        else:
            print(f"⚠️ Update failed: {data.get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Testing /config endpoint")
    print("=" * 60)
    print("\nMake sure Flask server is running on http://localhost:5000\n")
    
    test_config_get()
    test_config_post()
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)
