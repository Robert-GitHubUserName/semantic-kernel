#!/usr/bin/env python3
"""
Test script for the AI researcher app
"""

import requests
import json
import time

def test_chat_api():
    """Test the chat API functionality"""
    url = 'http://localhost:5001/api/chat'

    print("🧪 Testing AI Researcher App")
    print("=" * 40)

    # Test 1: Basic greeting
    print("\n1. Testing basic chat...")
    data1 = {'message': 'Hello! Can you help me with file operations?'}
    try:
        response1 = requests.post(url, json=data1, timeout=15)
        print(f"   Status: {response1.status_code}")
        result1 = response1.json()
        print(f"   AI Response: {result1.get('response', 'No response')[:100]}...")
    except Exception as e:
        print(f"   Error: {e}")
        return

    time.sleep(2)

    # Test 2: Memory test
    print("\n2. Testing memory retrieval...")
    data2 = {'message': 'What did I just ask you about?'}
    try:
        response2 = requests.post(url, json=data2, timeout=15)
        print(f"   Status: {response2.status_code}")
        result2 = response2.json()
        print(f"   AI Response: {result2.get('response', 'No response')[:100]}...")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 3: File operation
    print("\n3. Testing file creation...")
    data3 = {'message': 'Create a test file called hello.txt with content "Hello World!"'}
    try:
        response3 = requests.post(url, json=data3, timeout=15)
        print(f"   Status: {response3.status_code}")
        result3 = response3.json()
        print(f"   AI Response: {result3.get('response', 'No response')[:100]}...")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 4: Memory summary
    print("\n4. Testing memory summary...")
    try:
        response4 = requests.get('http://localhost:5001/api/chat/memory', timeout=10)
        print(f"   Status: {response4.status_code}")
        result4 = response4.json()
        print(f"   Memory Summary: {result4.get('memory', 'No summary')[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n✅ Testing complete!")

if __name__ == '__main__':
    test_chat_api()
