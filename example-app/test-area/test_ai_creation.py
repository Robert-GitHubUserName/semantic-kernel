#!/usr/bin/env python3
"""
Test script for AI file creation functionality
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_manager_app import AIAssistant, FileManager

async def test_ai_file_creation():
    """Test the AI file creation functionality."""
    print("Testing AI file creation...")
    print("=" * 50)

    # Initialize components
    file_manager = FileManager()
    ai_assistant = AIAssistant(file_manager)

    # Test request
    test_request = "write a short sci-fi poem to a file named sci-fi-poem.txt"

    print(f"Sending request: {test_request}")
    print("-" * 50)

    try:
        response = await ai_assistant.process_request(test_request)
        print(f"AI Response: {response}")
        print("-" * 50)

        # Check if file was created
        if os.path.exists("sci-fi-poem.txt"):
            print("✅ File 'sci-fi-poem.txt' was created successfully!")
            try:
                with open("sci-fi-poem.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                    print("File content:")
                    print("=" * 30)
                    print(content)
                    print("=" * 30)
            except UnicodeDecodeError:
                print("⚠️  File contains special characters, showing raw content:")
                with open("sci-fi-poem.txt", "rb") as f:
                    raw_content = f.read()
                    print(f"Raw bytes: {raw_content[:100]}...")

            # Get file info
            file_info = os.stat("sci-fi-poem.txt")
            print(f"File size: {file_info.st_size} bytes")
        else:
            print("❌ File 'sci-fi-poem.txt' was not created")
            print("Available files in directory:")
            for file in os.listdir("."):
                if os.path.isfile(file):
                    print(f"  - {file}")

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

async def test_memory_functionality():
    """Test the conversation memory functionality."""
    print("\n\nTesting AI Memory Functionality...")
    print("=" * 50)

    file_manager = FileManager()
    ai_assistant = AIAssistant(file_manager)

    # Multiple requests to test memory
    requests = [
        "Create a file called test1.txt with some content",
        "Now create another file called test2.txt",
        "What files have I created so far?",
        "Delete the test files I created"
    ]

    for i, request in enumerate(requests, 1):
        print(f"\nRequest {i}: {request}")
        try:
            response = await ai_assistant.process_request(request)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

    # Show memory status
    print(f"\nMemory status: {ai_assistant.get_memory_summary()}")

if __name__ == "__main__":
    print("AI File Manager Test Suite")
    print("=" * 60)

    # Run file creation test
    asyncio.run(test_ai_file_creation())

    # Run memory test
    asyncio.run(test_memory_functionality())

    print("\n" + "=" * 60)
    print("Test suite completed!")
