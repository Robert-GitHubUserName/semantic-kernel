"""
Flask Web Application

Web interface for the AI-powered file and browser automation system.
Provides a user-friendly dashboard to interact with MCP tools and AI capabilities.
"""

import asyncio
import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_socketio import SocketIO, emit
import json

# Import our AI agent and MCP modules
from main import AIAgent
from mcp_filesystem import MCPFileSystem
from mcp_browser import MCPBrowser

# Initialize Flask app
app = Flask(__name__)
print("DEBUG: Flask app initialized")
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change in production
print("DEBUG: Flask app configured")
socketio = SocketIO(app, cors_allowed_origins="*")
print("DEBUG: SocketIO initialized")

# Global AI agent instance
ai_agent = None

def get_ai_agent():
    """Get or create the AI agent instance."""
    global ai_agent
    print("DEBUG: get_ai_agent called")
    if ai_agent is None:
        print("DEBUG: Creating new AIAgent instance")
        try:
            ai_agent = AIAgent()
            print("DEBUG: AIAgent created successfully")
        except Exception as e:
            print(f"DEBUG: Error creating AIAgent: {e}")
            import traceback
            print(f"DEBUG: AIAgent creation traceback: {traceback.format_exc()}")
            raise
    else:
        print("DEBUG: Using existing AIAgent instance")
    return ai_agent

@app.route('/test')
def test():
    """Simple test route."""
    print("DEBUG: Test route called")
    return "Test route working"

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/file-operations')
def file_operations():
    """File operations page."""
    return render_template('file_operations.html')

@app.route('/browser-automation')
def browser_automation():
    """Browser automation page."""
    return render_template('browser_automation.html')

# API Routes

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test AI agent connection."""
    try:
        # Create event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        agent = get_ai_agent()
        ollama_result = loop.run_until_complete(agent.test_connection())
        sk_result = loop.run_until_complete(agent.test_semantic_kernel())

        loop.close()

        return jsonify({
            'success': True,
            'ollama': ollama_result,
            'semantic_kernel': sk_result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analyze-file', methods=['POST'])
def analyze_file():
    """Analyze a file using AI."""
    try:
        data = request.get_json()
        file_path = data.get('file_path', '')

        if not file_path:
            return jsonify({'success': False, 'error': 'File path is required'})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        agent = get_ai_agent()
        result = loop.run_until_complete(agent.analyze_file(file_path))

        loop.close()

        # Emit real-time update
        socketio.emit('analysis_complete', {'result': result})

        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    """Generate code using AI."""
    try:
        print("DEBUG: /api/generate-code route called")
        data = request.get_json()
        print(f"DEBUG: Request data: {data}")
        description = data.get('description', '')
        print(f"DEBUG: Description: '{description}'")

        if not description:
            return jsonify({'success': False, 'error': 'Description is required'})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        agent = get_ai_agent()
        result = loop.run_until_complete(agent.generate_code(description))

        loop.close()

        # Emit real-time update
        socketio.emit('code_generated', {'result': result})

        return jsonify({'success': True, 'result': result})
    except Exception as e:
        print(f"DEBUG: Exception in Flask route: {type(e).__name__}: {e}")
        import traceback
        print(f"DEBUG: Full traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/list-directory', methods=['POST'])
def list_directory():
    """List directory contents."""
    try:
        data = request.get_json()
        path = data.get('path', '.')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        fs = MCPFileSystem()
        result = loop.run_until_complete(fs.list_directory(path))

        loop.close()

        return jsonify({'success': True, 'files': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/read-file', methods=['POST'])
def read_file():
    """Read file contents."""
    try:
        data = request.get_json()
        file_path = data.get('file_path', '')

        if not file_path:
            return jsonify({'success': False, 'error': 'File path is required'})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        fs = MCPFileSystem()
        content = loop.run_until_complete(fs.read_file(file_path))

        loop.close()

        return jsonify({'success': True, 'content': content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/write-file', methods=['POST'])
def write_file():
    """Write content to file."""
    try:
        data = request.get_json()
        file_path = data.get('file_path', '')
        content = data.get('content', '')

        if not file_path:
            return jsonify({'success': False, 'error': 'File path is required'})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        fs = MCPFileSystem()
        success = loop.run_until_complete(fs.write_file(file_path, content))

        loop.close()

        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/navigate', methods=['POST'])
def navigate():
    """Navigate browser to URL."""
    try:
        data = request.get_json()
        url = data.get('url', '')

        if not url:
            return jsonify({'success': False, 'error': 'URL is required'})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        browser = MCPBrowser()
        success = loop.run_until_complete(browser.navigate(url))

        if success:
            # Get page content
            content = loop.run_until_complete(browser.get_page_content())
            socketio.emit('navigation_complete', {'url': url, 'content_length': len(content)})

        loop.close()

        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get-page-content', methods=['POST'])
def get_page_content():
    """Get current page content."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        browser = MCPBrowser()
        content = loop.run_until_complete(browser.get_page_content())

        loop.close()

        return jsonify({'success': True, 'content': content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/take-screenshot', methods=['POST'])
def take_screenshot():
    """Take a screenshot."""
    try:
        data = request.get_json()
        filename = data.get('filename', 'screenshot.png')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        browser = MCPBrowser()
        success = loop.run_until_complete(browser.take_screenshot(filename))

        loop.close()

        return jsonify({'success': success, 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/plan-web-task', methods=['POST'])
def plan_web_task():
    """Plan a web automation task."""
    try:
        data = request.get_json()
        task = data.get('task', '')

        if not task:
            return jsonify({'success': False, 'error': 'Task description is required'})

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        agent = get_ai_agent()
        plan = loop.run_until_complete(agent.plan_web_task(task))

        loop.close()

        return jsonify({'success': True, 'plan': plan})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# SocketIO event handlers

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('status', {'message': 'Connected to AI Agent server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')

@socketio.on('test_connection')
def handle_test_connection():
    """Handle connection test request."""
    # This will be handled asynchronously
    socketio.start_background_task(test_connection_background)

def test_connection_background():
    """Background task for testing connection."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        agent = get_ai_agent()
        ollama_result = loop.run_until_complete(agent.test_connection())
        sk_result = loop.run_until_complete(agent.test_semantic_kernel())

        loop.close()

        socketio.emit('connection_test_result', {
            'ollama': ollama_result,
            'semantic_kernel': sk_result
        })
    except Exception as e:
        socketio.emit('connection_test_result', {'error': str(e)})

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Make sure Ollama is running with gemma3:latest model")
    print("Make sure MCP servers are running:")
    print("  - filesystem-operations-mcp")
    print("  - npx @playwright/mcp@latest")

    # Run with SocketIO support
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
