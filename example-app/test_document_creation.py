#!/usr/bin/env python3
"""
Test script for document creation from web research.
This demonstrates how to use the new create-document API endpoint.
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:5001/api/research/create-document"

# Example: Create a document from multiple URLs
def test_create_document():
    """Test creating a document from web URLs."""
    
    # Example URLs to scrape and screenshot
    test_data = {
        "urls": [
            "https://example.com",
            "https://www.wikipedia.org"
        ],
        "title": "My Web Research Document"
    }
    
    print("Sending request to create document...")
    print(f"URLs: {test_data['urls']}")
    print(f"Title: {test_data['title']}")
    print("-" * 60)
    
    try:
        response = requests.post(API_URL, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ Document created successfully!")
            print(f"  - Filename: {result['filename']}")
            print(f"  - Path: {result['document_path']}")
            print(f"  - URLs processed: {result['urls_processed']}")
            print(f"  - Screenshots captured: {len(result['screenshots'])}")
            print(f"  - Screenshot files: {', '.join(result['screenshots'])}")
            print(f"\n{result['message']}")
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"\n✗ Exception: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Web Research Document Creation Test")
    print("=" * 60)
    test_create_document()
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
