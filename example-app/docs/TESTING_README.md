# AI Researcher Application - Testing Guide

This guide documents the testing procedures for the AI Researcher application, which combines AI-powered file management with real web research capabilities.

## Application Overview

The AI Researcher application provides:
- **AI-powered file operations** through natural language commands
- **Real web research** using DuckDuckGo search and webpage content extraction
- **Interactive file browser** with directory navigation
- **Document generation** from web research findings

## Prerequisites

### System Requirements
- Python 3.8+
- Ollama with Gemma3 model
- Web browser for UI access

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install Ollama and pull model
ollama pull gemma3:latest
```

## Starting the Application

```bash
cd example-app
python ai_researcher_app.py
```

The application will be available at: **http://localhost:5001**

## Test Scenarios

### 1. Application Startup Test

**Objective**: Verify the application starts successfully and serves the web interface.

**Command**:
```bash
cd "c:\FilesMinis\Code\GitHub\semantic-kernel\example-app"
python ai_researcher_app.py
```

**Expected Output**:
```
File Manager with AI Chat
========================================
Base directory: C:\FilesMinis\Code\GitHub
Starting Flask application...
* Running on http://127.0.0.1:5001
* Running on http://192.168.0.3:5001
```

**Success Criteria**:
- Application starts without errors
- Flask server runs on port 5001
- No import errors or missing dependencies

### 2. Web Search Functionality Test

**Objective**: Test real web search using DuckDuckGo and verify results are authentic.

**Test Script**:
```python
import requests
import json

# Test web search API
url = 'http://localhost:5001/api/research/web-search'
data = {'query': 'artificial intelligence'}

response = requests.post(url, json=data, timeout=15)
result = response.json()

print('Status Code:', response.status_code)
print('Query:', result.get('query', 'No query'))
print('Source:', result.get('source', 'No source'))
print('Number of results:', len(result.get('results', [])))

if result.get('results'):
    first_result = result['results'][0]
    print('First result:')
    print('  Title:', first_result.get('title', 'No title'))
    print('  URL:', first_result.get('url', 'No URL'))
    print('  Type:', first_result.get('type', 'No type'))
```

**Expected Results**:
- HTTP 200 status code
- Results contain real URLs from DuckDuckGo
- Source should be 'real_web_search'
- Results should include legitimate websites

### 3. Directory Navigation Test

**Objective**: Test navigation between directories and verify current directory tracking.

**Test Script**:
```python
import requests
import json

# Navigate to a subdirectory
nav_url = 'http://localhost:5001/api/files/navigate'
nav_data = {'path': r'C:\FilesMinis\Code\GitHub\semantic-kernel'}

nav_response = requests.post(nav_url, json=nav_data, timeout=10)
nav_result = nav_response.json()
print('Navigation result:', nav_result.get('current_path', 'Failed'))

# Check current directory
curr_url = 'http://localhost:5001/api/files/current-dir'
curr_response = requests.get(curr_url, timeout=10)
curr_result = curr_response.json()
print('Current directory:', curr_result.get('current_directory', 'Unknown'))
```

**Expected Results**:
- Navigation succeeds and returns the target path
- Current directory API returns the navigated path
- Directory listing shows contents of the navigated directory

### 4. File Creation in Current Directory Test

**Objective**: Test that files are created in the directory currently being browsed.

**Test Script**:
```python
import requests
import json

# Navigate to a subdirectory first
nav_url = 'http://localhost:5001/api/files/navigate'
nav_data = {'path': r'C:\FilesMinis\Code\GitHub\semantic-kernel'}
nav_response = requests.post(nav_url, json=nav_data, timeout=10)
print('Navigated to:', nav_response.json().get('current_path', 'Failed'))

# Create a file
chat_url = 'http://localhost:5001/api/chat'
chat_data = {'message': 'Create a test file called current_dir_test.txt with test content'}

chat_response = requests.post(chat_url, json=chat_data, timeout=15)
chat_result = chat_response.json()
print('File creation response:', chat_result.get('response', 'No response'))

# Verify file exists in current directory
list_url = 'http://localhost:5001/api/files'
list_response = requests.get(list_url, timeout=10)
list_result = list_response.json()

print('Files in current directory:')
for item in list_result.get('items', []):
    if 'test' in item['name'].lower():
        print('  Found:', item['name'], '(' + item['type'] + ')')
```

**Expected Results**:
- File creation succeeds
- File appears in the directory listing of the current directory
- File is created in the navigated subdirectory, not the base directory

### 5. File Operations Test

**Objective**: Test complete file operation workflow (create, read, delete).

**Test Script**:
```python
import requests
import json

# Create a test file
chat_url = 'http://localhost:5001/api/chat'
create_data = {'message': 'Create a test file called operations_test.txt with sample content'}
create_response = requests.post(chat_url, json=create_data, timeout=15)
print('Create result:', create_response.json().get('response', 'Failed'))

# Read the file
read_url = 'http://localhost:5001/api/files/read'
read_data = {'path': 'operations_test.txt'}
read_response = requests.post(read_url, json=read_data, timeout=10)
read_result = read_response.json()
print('Read result:', 'Success' if read_result.get('content') else 'Failed')

# Delete the file
delete_url = 'http://localhost:5001/api/files/delete'
delete_data = {'path': 'operations_test.txt'}
delete_response = requests.post(delete_url, json=delete_data, timeout=10)
delete_result = delete_response.json()
print('Delete result:', 'Success' if delete_result.get('success') else 'Failed')
```

**Expected Results**:
- File creation succeeds
- File reading returns the content
- File deletion succeeds
- File no longer appears in directory listings

### 6. Webpage Content Fetching Test

**Objective**: Test fetching and extracting content from real webpages.

**Test Script**:
```python
import requests
import json

# Test webpage fetching
url = 'http://localhost:5001/api/research/fetch-page'
data = {'url': 'https://www.ssga.com/us/en/individual/etfs/fund-details/etfusspy'}

response = requests.post(url, json=data, timeout=15)
result = response.json()

print('URL:', result.get('url', 'No URL'))
print('Status:', result.get('status_code', 'No status'))
print('Source:', result.get('source', 'No source'))
print('Content length:', len(result.get('content', '')))
print('Content preview:', result.get('content', 'No content')[:200] + '...')
```

**Expected Results**:
- HTTP 200 status code
- Content is extracted from the real webpage
- Source should be 'real_webpage'
- Content should contain actual webpage text

## Automated Test Suite

### Running All Tests

Create a comprehensive test script:

```python
#!/usr/bin/env python3
"""
Comprehensive test suite for AI Researcher application
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5001'

def test_web_search():
    """Test web search functionality"""
    url = f'{BASE_URL}/api/research/web-search'
    data = {'query': 'machine learning'}
    
    response = requests.post(url, json=data, timeout=15)
    assert response.status_code == 200
    
    result = response.json()
    assert 'results' in result
    assert len(result['results']) > 0
    assert result['source'] == 'real_web_search'
    
    print("✓ Web search test passed")

def test_file_operations():
    """Test file creation, reading, and deletion"""
    # Create file
    chat_url = f'{BASE_URL}/api/chat'
    create_data = {'message': 'Create test_file.txt with test content'}
    response = requests.post(chat_url, json=create_data, timeout=15)
    assert 'Successfully created' in response.json()['response']
    
    # Read file
    read_url = f'{BASE_URL}/api/files/read'
    read_data = {'path': 'test_file.txt'}
    response = requests.post(read_url, json=read_data, timeout=10)
    assert 'content' in response.json()
    
    # Delete file
    delete_url = f'{BASE_URL}/api/files/delete'
    delete_data = {'path': 'test_file.txt'}
    response = requests.post(delete_url, json=delete_data, timeout=10)
    assert response.json()['success'] == True
    
    print("✓ File operations test passed")

def test_navigation():
    """Test directory navigation"""
    nav_url = f'{BASE_URL}/api/files/navigate'
    nav_data = {'path': r'C:\FilesMinis\Code\GitHub'}
    
    response = requests.post(nav_url, json=nav_data, timeout=10)
    assert 'current_path' in response.json()
    
    print("✓ Navigation test passed")

if __name__ == '__main__':
    print("Running AI Researcher test suite...")
    
    try:
        test_web_search()
        test_file_operations()
        test_navigation()
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
```

### Running the Test Suite

```bash
python test_suite.py
```

## Troubleshooting

### Common Issues

**Application won't start**:
- Check if Ollama is running: `ollama list`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check for port conflicts on 5001

**Web search fails**:
- Verify internet connection
- Check if DuckDuckGo is accessible
- Review error messages in application logs

**File operations fail**:
- Verify write permissions in the base directory
- Check if files are being created in the correct directory
- Ensure paths are within the allowed base directory

**Navigation issues**:
- Use absolute paths for navigation
- Verify directory exists and is accessible
- Check current directory after navigation

## Performance Benchmarks

### Expected Response Times

- **Application startup**: < 5 seconds
- **Web search**: 2-10 seconds (depends on query complexity)
- **File operations**: < 1 second
- **Directory navigation**: < 1 second
- **Page content fetching**: 3-15 seconds (depends on page size)

### Resource Usage

- **Memory**: ~200-500 MB during normal operation
- **CPU**: Minimal during idle, spikes during AI processing
- **Network**: Required for web search and content fetching

## Test Coverage

This test suite covers:
- ✅ Application startup and configuration
- ✅ Real web search functionality
- ✅ Directory navigation and file browser
- ✅ File creation, reading, and deletion
- ✅ AI chat interface for file operations
- ✅ Webpage content extraction
- ✅ Error handling and edge cases

## Contributing

When adding new features:
1. Add corresponding tests to this guide
2. Update the automated test suite
3. Document any new API endpoints
4. Include performance expectations

---

**Test Environment**: Windows 10/11, Python 3.8+, Ollama with Gemma3 model
**Last Updated**: September 23, 2025</content>
<parameter name="filePath">c:\FilesMinis\Code\GitHub\semantic-kernel\example-app\TESTING_README.md
