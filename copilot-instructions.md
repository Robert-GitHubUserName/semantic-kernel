# Copilot Instructions: AI Researcher App with Semantic Kernel Memory

## Overview
This project implements a comprehensive AI-powered file management and research application featuring:

- **Modern Vector Store Memory**: Production-ready Semantic Kernel vector-based conversation memory
- **Ollama Integration**: Uses Gemma3:latest model for AI responses and nomic-embed-text for embeddings
- **Flask Web Interface**: Interactive file browser with real-time chat
- **Web Research Capabilities**: Real web scraping and content analysis
- **File Operations**: Complete CRUD operations with security controls
- **Conversational AI**: Natural language responses with persistent vector-based memory context

The application demonstrates advanced AI orchestration using Microsoft Semantic Kernel's modern Vector Store APIs, with persistent memory that enables the AI to remember conversations and provide personalized responses.

---

## Project Structure
```
semantic-kernel/
├── example-app/
│   ├── ai_researcher_app.py          # Main Flask application
│   ├── requirements.txt              # Python dependencies
│   ├── templates/
│   │   └── ai_researcher.html        # Web interface
│   ├── static/                       # CSS/JS assets
│   ├── data/                         # Application data directory
│   ├── test-area/                    # Testing workspace
│   └── README.md                     # Application documentation
├── copilot-instructions.md           # This file
└── README.md                         # Project documentation
```

---

## Key Features Implemented

### ✅ Modern Vector Store Memory System
- **InMemoryCollection**: Production-ready vector-based memory storage
- **Custom MemoryRecord Model**: VectorStoreField-annotated dataclass for structured data
- **Intelligent Retrieval**: Context-aware memory search with vector embeddings
- **Persistent Context**: Conversations maintained across sessions with modern APIs

### ✅ AI Assistant Capabilities
- **Conversational Responses**: Natural language for greetings, questions, memory recall
- **File Operations**: JSON-driven file creation, reading, writing, deletion
- **Content Generation**: AI-powered poem/story/code generation
- **Web Research**: Real DuckDuckGo search and webpage content extraction

### ✅ Web Interface
- **Real-time Chat**: WebSocket-powered AI conversations
- **File Browser**: Interactive directory navigation and file management
- **Research Tools**: Web search and content analysis interfaces
- **Memory Management**: View and clear conversation history

---

## Setup Instructions

### 1. Environment Setup
```bash
# Navigate to project directory
cd semantic-kernel/example-app

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `flask>=3.0` - Web framework
- `flask-socketio>=5.3` - Real-time communication
- `semantic-kernel>=1.18.0` - AI orchestration
- `ollama>=0.3.0` - Local AI model interface
- `requests` - HTTP client for web research
- `beautifulsoup4` - HTML parsing

### 3. Setup AI Services

**Option A: Ollama (Local, Free)**
```bash
# Install Ollama (if not already installed)
# Download from: https://ollama.ai/download

# Pull the Gemma3 model for chat
ollama pull gemma3:latest

# Pull the embeddings model for vector storage
ollama pull nomic-embed-text

# Test the models
ollama run gemma3:latest
ollama run nomic-embed-text
```

**Option B: Azure OpenAI (Microsoft Recommended for Production)**
```bash
# Set environment variables
export AZURE_OPENAI_API_KEY="your-azure-openai-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-02-01"

# Deploy embeddings model (text-embedding-ada-002 or text-embedding-3-small)
# Deploy chat model (gpt-4, gpt-3.5-turbo, or gpt-4-turbo)
```

**Option C: Direct OpenAI API (Microsoft Recommended for Development)**
```bash
# Set environment variable
export OPENAI_API_KEY="your-openai-api-key"
```

### 4. Run the Application
```bash
python ai_researcher_app.py
```

The application will start on `http://127.0.0.1:5001`

---

## Microsoft-Recommended Embedding Providers

Instead of using Ollama for embeddings, Microsoft recommends using cloud-based embedding services for production applications:

### Azure OpenAI Embeddings (Recommended for Enterprise)

```python
from semantic_kernel.connectors.ai.azure_open_ai import AzureOpenAITextEmbedding
import openai

# Initialize Azure OpenAI client
azure_client = openai.AsyncAzureOpenAI(
    api_key="your-azure-openai-api-key",
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_version="2024-02-01"
)

# Initialize embeddings service
embeddings_service = AzureOpenAITextEmbedding(
    deployment_name="text-embedding-ada-002",  # or text-embedding-3-small
    service_id="azure-embeddings",
    async_client=azure_client
)

# Use with InMemoryCollection
memory = InMemoryCollection(
    record_type=MemoryRecord,
    collection_name="ai_memory",
    embedding_generator=embeddings_service
)
```

**Benefits:**
- Enterprise-grade security and compliance
- Scalable and managed service
- Integrated with Azure ecosystem
- Pay-per-use pricing

### Direct OpenAI API (Recommended for Development/Testing)

```python
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
import openai

# Initialize OpenAI client
openai_client = openai.AsyncOpenAI(
    api_key="your-openai-api-key"
)

# Initialize embeddings service
embeddings_service = OpenAITextEmbedding(
    ai_model_id="text-embedding-ada-002",  # or text-embedding-3-small
    service_id="openai-embeddings",
    async_client=openai_client
)

# Use with InMemoryCollection
memory = InMemoryCollection(
    record_type=MemoryRecord,
    collection_name="ai_memory",
    embedding_generator=embeddings_service
)
```

**Benefits:**
- Simple setup and configuration
- High-quality embeddings
- Well-documented API
- Good for prototyping

### Environment Variables Setup

```bash
# For Azure OpenAI
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-02-01"

# For Direct OpenAI
export OPENAI_API_KEY="your-openai-key"
```

**Why Microsoft Recommends Cloud Providers:**
- **Reliability**: 99.9% uptime SLAs
- **Performance**: Optimized infrastructure for embeddings
- **Security**: Enterprise-grade security features
- **Scalability**: Auto-scaling based on demand
- **Maintenance**: No local model management required

---

## How It Works

### Modern Vector Store Architecture
```
User Input → Semantic Kernel → Vector Search → Context Enrichment → AI Response → Vector Storage
```

1. **Input Processing**: User messages are processed through regex patterns for file operations
2. **Vector Retrieval**: Relevant conversation history retrieved using vector similarity search
3. **Context Building**: Recent history + relevant vector memories form the AI prompt
4. **AI Response**: Gemma3 model generates contextual responses
5. **Vector Storage**: New exchanges stored as vectors for future retrieval using upsert API

### File Operations Flow
```
User Request → Regex Matching → Direct File Action → Success Response
                                      ↓
JSON Response → FileManager → File Operation → Result
```

### Web Research Flow
```
Search Query → DuckDuckGo API → Parse Results → Return Structured Data
Webpage URL → HTTP Request → BeautifulSoup Parse → Content Extraction
```

---

## Key Code Components

### AIAssistant Class
- **Vector Store Management**: Handles conversation storage and retrieval using InMemoryCollection
- **MemoryRecord Model**: Custom dataclass with VectorStoreField annotations for structured data
- **Request Processing**: Routes between conversational and operational responses
- **Vector Operations**: Uses upsert() for storage and search() for retrieval with embeddings

### FileManager Class
- **Security Controls**: Path validation and access restrictions
- **File Operations**: CRUD operations with proper error handling
- **Directory Navigation**: Safe workspace navigation

### Web Research Module
- **Search Integration**: Real web search with DuckDuckGo
- **Content Extraction**: HTML parsing and text extraction
- **Fallback Handling**: AI-generated content when web requests fail

---

## Example Code Snippets

This section provides reusable code patterns for building similar AI-powered applications. Each snippet demonstrates key architectural patterns that can be adapted for different purposes.

### 1. Modern Vector Store Memory Setup

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding
from semantic_kernel.data.vector import vectorstoremodel, VectorStoreField
from semantic_kernel.connectors.in_memory import InMemoryCollection
from dataclasses import dataclass
from typing import Annotated, Optional
import openai

@vectorstoremodel
@dataclass
class MemoryRecord:
    """Custom memory record for vector storage."""
    id: Annotated[str, VectorStoreField('key')]
    text: Annotated[str, VectorStoreField('data', is_full_text_indexed=True)]
    description: Annotated[str, VectorStoreField('data')]
    timestamp: Annotated[Optional[str], VectorStoreField('data')] = None

class AIMemorySystem:
    """AI assistant with vector-based memory."""
    
    def __init__(self):
        # Configure Ollama client
        self.ollama_client = openai.AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
        
        # Initialize embeddings service
        # Option A: Using Ollama (current implementation)
        embeddings_service = OpenAITextEmbedding(
            ai_model_id="nomic-embed-text",
            service_id="ollama-embeddings",
            async_client=self.ollama_client
        )
        
        # Option B: Using Azure OpenAI (Microsoft recommended)
        # from semantic_kernel.connectors.ai.azure_open_ai import AzureOpenAITextEmbedding
        # 
        # azure_client = openai.AsyncAzureOpenAI(
        #     api_key="your-azure-openai-api-key",
        #     azure_endpoint="https://your-resource.openai.azure.com/",
        #     api_version="2024-02-01"
        # )
        # 
        # embeddings_service = AzureOpenAITextEmbedding(
        #     deployment_name="text-embedding-ada-002",  # or text-embedding-3-small
        #     service_id="azure-embeddings",
        #     async_client=azure_client
        # )
        
        # Option C: Using Direct OpenAI API (Microsoft recommended)
        # openai_client = openai.AsyncOpenAI(
        #     api_key="your-openai-api-key"
        # )
        # 
        # embeddings_service = OpenAITextEmbedding(
        #     ai_model_id="text-embedding-ada-002",  # or text-embedding-3-small
        #     service_id="openai-embeddings",
        #     async_client=openai_client
        # )
        
        # Initialize vector store
        self.collection_name = "my_app_memory"
        self.memory = InMemoryCollection(
            record_type=MemoryRecord,
            collection_name=self.collection_name,
            embedding_generator=embeddings_service
        )
        
        # Conversation tracking
        self.conversation_history = []
        self.max_memory_items = 10
    
    async def save_memory(self, user_input: str, ai_response: str):
        """Save conversation to vector store."""
        memory_text = f"User: {user_input}\nAI: {ai_response}"
        memory_id = f"conv_{len(self.conversation_history)}_{hash(user_input) % 10000}"
        
        record = MemoryRecord(
            id=memory_id,
            text=memory_text,
            description=f"Conversation about: {user_input[:50]}...",
            timestamp=datetime.now().isoformat()
        )
        
        await self.memory.upsert([record])
    
    async def retrieve_relevant_memories(self, query: str, limit: int = 5):
        """Retrieve relevant memories using vector similarity."""
        results = await self.memory.search(values=query, top=limit)
        return [result.text for result in results]
```

### 2. AI Assistant with Semantic Kernel Integration

```python
from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

class AIAssistant:
    """AI assistant with memory and function calling."""
    
    def __init__(self, memory_system):
        self.memory_system = memory_system
        self.kernel = Kernel()
        
        # Add chat service
        chat_service = OpenAIChatCompletion(
            ai_model_id="gemma3:latest",
            service_id="ollama-chat",
            async_client=self.ollama_client
        )
        self.kernel.add_service(chat_service)
        
        # Register functions
        self._register_functions()
    
    def _register_functions(self):
        """Register semantic functions for different tasks."""
        
        # General assistant function
        assistant_prompt = """
        You are a helpful AI assistant with conversation memory.
        
        RECENT CONVERSATION:
        {{$conversation_history}}
        
        RELEVANT PREVIOUS CONTEXT:
        {{$relevant_memories}}
        
        USER REQUEST: {{$user_request}}
        
        Respond naturally and helpfully. Use the conversation context to provide personalized responses.
        """
        
        self.kernel.add_function(
            plugin_name="assistant",
            function_name="respond",
            prompt=assistant_prompt
        )
        
        # Content generation function
        content_prompt = """
        Generate the requested content based on the user's description.
        Provide only the content itself without explanations.
        
        Request: {{$content_request}}
        """
        
        self.kernel.add_function(
            plugin_name="generator",
            function_name="create_content",
            prompt=content_prompt
        )
    
    async def process_request(self, user_request: str) -> str:
        """Process user request with memory context."""
        
        # Get relevant memories
        relevant_memories = await self.memory_system.retrieve_relevant_memories(user_request)
        
        # Format conversation history
        history_text = "\n".join([
            f"User: {user_msg}\nAI: {ai_response}"
            for user_msg, ai_response in self.memory_system.conversation_history[-5:]
        ])
        
        # Combine memories
        memory_context = "\n".join([f"Previous: {mem}" for mem in relevant_memories])
        
        # Invoke AI with context
        arguments = KernelArguments(
            user_request=user_request,
            conversation_history=history_text,
            relevant_memories=memory_context
        )
        
        result = await self.kernel.invoke(
            function_name="respond",
            plugin_name="assistant",
            arguments=arguments
        )
        
        response = str(result)
        
        # Save to memory
        await self.memory_system.save_memory(user_request, response)
        self.memory_system.conversation_history.append((user_request, response))
        
        return response
```

### 3. Secure File Operations Manager

```python
from pathlib import Path
from typing import Dict, List
import os
import platform
import subprocess
from datetime import datetime

class SecureFileManager:
    """Secure file operations with path validation."""
    
    def __init__(self, base_path: str = None):
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Use current directory as base
            self.base_path = Path.cwd()
        
        self.current_path = self.base_path
    
    def _validate_path(self, path: Path) -> bool:
        """Validate path is within allowed boundaries."""
        try:
            resolved = path.resolve()
            return str(resolved).startswith(str(self.base_path))
        except:
            return False
    
    def list_directory(self, path: str = None) -> Dict:
        """List directory contents safely."""
        try:
            target_path = Path(path) if path else self.current_path
            target_path = target_path.resolve()
            
            if not self._validate_path(target_path):
                return {"error": "Access denied"}
            
            if not target_path.exists() or not target_path.is_dir():
                return {"error": "Invalid directory"}
            
            items = []
            for item in sorted(target_path.iterdir()):
                try:
                    stat = item.stat()
                    items.append({
                        "name": item.name,
                        "path": str(item),
                        "type": "directory" if item.is_dir() else "file",
                        "size": stat.st_size if item.is_file() else 0,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except (OSError, PermissionError):
                    continue
            
            return {
                "current_path": str(target_path),
                "items": items
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def read_file(self, file_path: str) -> Dict:
        """Read file contents safely."""
        try:
            path = (self.current_path / file_path).resolve()
            
            if not self._validate_path(path):
                return {"error": "Access denied"}
            
            if not path.exists() or not path.is_file():
                return {"error": "File not found"}
            
            # Check if text file
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"content": content}
            except UnicodeDecodeError:
                return {"error": "Binary file"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def write_file(self, file_path: str, content: str) -> Dict:
        """Write content to file safely."""
        try:
            path = (self.current_path / file_path).resolve()
            
            if not self._validate_path(path):
                return {"error": "Access denied"}
            
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {"success": True}
            
        except Exception as e:
            return {"error": str(e)}
    
    def open_file(self, file_path: str) -> Dict:
        """Open file in default application."""
        try:
            path = (self.current_path / file_path).resolve()
            
            if not self._validate_path(path):
                return {"error": "Access denied"}
            
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
            
            return {"success": True}
            
        except Exception as e:
            return {"error": str(e)}
```

### 4. Flask Web Application with SocketIO

```python
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import asyncio

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize your components
file_manager = SecureFileManager()
ai_assistant = AIAssistant(memory_system)

@app.route('/')
def index():
    """Main application page."""
    return render_template('index.html')

# File management routes
@app.route('/api/files')
def get_files():
    """Get directory listing."""
    result = file_manager.list_directory()
    return jsonify(result)

@app.route('/api/files/read', methods=['POST'])
def read_file():
    """Read file contents."""
    data = request.get_json()
    result = file_manager.read_file(data.get('path', ''))
    return jsonify(result)

@app.route('/api/files/write', methods=['POST'])
def write_file():
    """Write to file."""
    data = request.get_json()
    result = file_manager.write_file(
        data.get('path', ''), 
        data.get('content', '')
    )
    return jsonify(result)

# AI chat route
@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat message."""
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message required'})
    
    # Run async AI processing
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        response = loop.run_until_complete(
            ai_assistant.process_request(message)
        )
        loop.close()
        return jsonify({'response': response})
    except Exception as e:
        loop.close()
        return jsonify({'error': str(e)})

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('status', {'message': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')

if __name__ == '__main__':
    print("Starting AI-powered web application...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

### 5. Web Research and Content Extraction

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

class WebResearcher:
    """Web research and content extraction."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_web(self, query: str, max_results: int = 5) -> Dict:
        """Perform web search using DuckDuckGo."""
        try:
            search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Extract search results
            result_links = soup.find_all('a', class_='result__a')
            result_snippets = soup.find_all('a', class_='result__snippet')
            
            for i, link in enumerate(result_links[:max_results]):
                title = link.get_text().strip()
                url = link.get('href', '')
                
                snippet = ""
                if i < len(result_snippets):
                    snippet = result_snippets[i].get_text().strip()
                
                if url and title:
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet
                    })
            
            return {
                'query': query,
                'results': results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e), 'query': query}
    
    def fetch_webpage(self, url: str) -> Dict:
        """Fetch and extract webpage content."""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else "No title"
            
            # Find main content
            main_content = ""
            content_selectors = ['main', 'article', '.content', '#content']
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    main_content = content_elem.get_text(separator='\n', strip=True)
                    break
            
            if not main_content:
                body = soup.find('body')
                main_content = body.get_text(separator='\n', strip=True) if body else ""
            
            # Clean content
            lines = [line.strip() for line in main_content.split('\n') if line.strip()]
            clean_content = '\n'.join(lines[:30])  # Limit content
            
            return {
                'url': url,
                'title': title,
                'content': clean_content,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e), 'url': url}
```

### 6. Flask Routes for Web Research

```python
# Add to your Flask app

@app.route('/api/research/web-search', methods=['POST'])
def web_search_api():
    """Web search endpoint."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query required'}), 400
        
        researcher = WebResearcher()
        results = researcher.search_web(query)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/research/fetch-page', methods=['POST'])
def fetch_page_api():
    """Fetch webpage content endpoint."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL required'}), 400
        
        researcher = WebResearcher()
        result = researcher.fetch_webpage(url)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 7. Complete Application Initialization

```python
# main.py - Complete application setup

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import asyncio

# Import your components
from ai_memory import AIMemorySystem
from ai_assistant import AIAssistant
from file_manager import SecureFileManager
from web_research import WebResearcher

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-app-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
memory_system = AIMemorySystem()
ai_assistant = AIAssistant(memory_system)
file_manager = SecureFileManager()
researcher = WebResearcher()

# Include all the routes from previous snippets...

if __name__ == '__main__':
    print("🚀 Starting AI-Powered Application")
    print("=" * 50)
    print("Features:")
    print("• AI chat with vector memory")
    print("• Secure file management")
    print("• Web research capabilities")
    print("• Real-time updates via WebSocket")
    print(f"• Base directory: {file_manager.base_path}")
    print("=" * 50)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

---

## Testing the Application

### Basic Functionality
```bash
# Start the app
python ai_researcher_app.py

# Open browser to http://127.0.0.1:5001

# Test conversational AI
"Hello" → Should get natural greeting
"What is my name?" → Should remember from conversation history

# Test file operations
"Create test.txt with Hello World" → File created successfully
"List files" → Shows directory contents
```

### Memory Testing
```bash
# Have a conversation
"My name is Alice"
"What is my name?" → Should respond with "Alice"

# Check memory
GET /api/chat/memory → Shows conversation history
```

### Web Research Testing
```bash
# Test web search
POST /api/research/web-search
{"query": "artificial intelligence"}

# Test webpage content
POST /api/research/fetch-page
{"url": "https://example.com"}
```

---

## Advanced Features

### Semantic Vector Search
- Uses vector embeddings for intelligent memory retrieval
- Filters memories by relevance score (>0.3) using cosine similarity
- Combines recent history with relevant past context from vector store

### Dual Response System
- **Conversational**: Natural language for social interactions
- **Operational**: JSON actions for file/web operations
- **Smart Detection**: Automatically routes based on request type

### Security Features
- Path validation prevents directory traversal
- Base directory restrictions
- File type validation for text/binary content

---

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure virtual environment is activated
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**Ollama Connection Issues:**
```bash
# Check Ollama is running
ollama list
ollama run gemma3:latest

# Verify model is available
curl http://localhost:11434/api/tags
```

**Memory Not Working:**
- Check that Semantic Kernel Vector Store imports are correct
- Verify InMemoryCollection and MemoryRecord model are properly initialized
- Check console logs for vector store upsert/search errors
- Ensure Ollama embeddings service is running for vector generation

**File Operations Failing:**
- Verify current working directory permissions
- Check base path configuration in FileManager
- Ensure file paths are within allowed directories

---

## Development Notes

### Architecture Decisions
- **Flask + SocketIO**: Real-time web interface with async support
- **Semantic Kernel Vector Stores**: Modern AI orchestration with production-ready memory
- **InMemoryCollection**: High-performance vector storage with custom data models
- **Ollama Embeddings**: Local AI model for privacy and cost efficiency
- **Regex + AI**: Hybrid approach for reliable file operations

### Future Enhancements
- **Persistent Storage**: Database integration for long-term memory
- **Multi-user Support**: User sessions and isolated memories
- **Advanced Research**: Academic paper search and analysis
- **Plugin System**: Extensible architecture for new capabilities

---

## Best Practices Implemented

- **Type Hints**: Full type annotation for better IDE support
- **Error Handling**: Comprehensive exception catching and logging
- **Modular Design**: Separated concerns (FileManager, AIAssistant, Web routes)
- **Security**: Path validation and access controls
- **Documentation**: Inline docstrings and comprehensive README
- **Async/Await**: Proper asynchronous programming patterns

---

This application demonstrates a production-ready AI assistant with advanced memory capabilities, suitable for file management, research, and conversational AI tasks. The Semantic Kernel integration provides intelligent context awareness, making interactions feel natural and personalized.

🎯 **Ready to use at:** `http://127.0.0.1:5001`
