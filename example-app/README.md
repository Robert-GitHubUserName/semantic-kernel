# AI Researcher - File Management & Web Research Tool

A comprehensive Python web application combining **AI-powered file management**, **intelligent web research**, and **document creation** using Microsoft Semantic Kernel's modern Vector Stores and local Ollama AI models.

## 🚀 Features

- **AI-Powered File Operations**: Create, read, write, and manage files through natural language commands
- **Intelligent Web Research**: Perform real web searches and extract content from actual websites
- **Document Generation**: Create comprehensive research documents from web findings
- **Real-time Chat Interface**: Interactive AI assistant with conversation memory
- **Modern Vector Store Memory**: Advanced conversation memory using Semantic Kernel Vector Stores with embeddings
- **Intelligent Context Retrieval**: AI remembers and retrieves relevant context using vector similarity search
- **Secure File System**: Configurable base directory with navigation controls
- **Modern Web UI**: Responsive interface with tabbed navigation and live updates

## 🏗️ Architecture

```
example-app/
├── ai_researcher_app.py      # Main Flask application with AI integration
├── requirements.txt          # Python dependencies
├── templates/
│   └── ai_researcher.html    # Main web interface
├── static/                   # CSS, JS, and assets
├── test-area/               # Archived alternative implementations
├── data/                    # Application data storage
└── README.md
```

### Memory System
- **Vector Store**: Uses Semantic Kernel's modern InMemoryCollection for conversation memory
- **Embeddings**: Leverages Ollama's nomic-embed-text model for semantic understanding
- **Context Retrieval**: Vector similarity search enables intelligent context-aware responses
- **Data Model**: Custom MemoryRecord with full-text indexing and metadata storage

## 📋 Prerequisites

### System Requirements
- **Python 3.8+**
- **Ollama** (for local AI models)

### Install Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from: https://ollama.ai/download
```

## 🛠️ Installation & Setup

### 1. Set Up Python Virtual Environment
```bash
cd example-app
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Ollama Model
```bash
# Pull the Gemma3 model
ollama pull gemma3:latest

# Test the model
ollama run gemma3:latest
```

## 🚀 Running the Application

### Start the AI Researcher Application
```bash
python ai_researcher_app.py
```

Access at: **http://localhost:5001**

## 🎯 Usage

### File Management Tab
- **Browse Files**: Navigate through your project directory structure
- **AI File Creation**: Use natural language to create files (e.g., "Create a Python script that prints hello world")
- **File Operations**: Read, write, delete, and manage files
- **Open Files**: Launch files in their default applications

### Web Research Tab
- **Real Web Search**: Search the internet using actual search engines (DuckDuckGo)
- **Content Extraction**: Fetch and analyze real webpage content
- **Research Documents**: Generate comprehensive documents from search results
- **Source Verification**: All results come from legitimate, working URLs

### AI Chat Tab
- **Natural Language Commands**: Chat with AI assistant for file and research tasks
- **Vector Store Memory**: Advanced conversation memory using embeddings for semantic understanding
- **Intelligent Context Retrieval**: AI retrieves relevant past conversations using vector similarity
- **Smart Automation**: AI can perform complex multi-step operations with persistent memory

## 🔧 Configuration

### Base Directory
The application uses `C:\FilesMinis\Code\GitHub` as the base directory for file operations. This can be modified in `ai_researcher_app.py`:

```python
# In FileManager.__init__()
self.base_path = Path(r"C:\FilesMinis\Code\GitHub")  # Change this path as needed
```

### AI Model Configuration
Modify the AI model in `ai_researcher_app.py`:

```python
self.service = OpenAIChatCompletion(
    ai_model_id="gemma3:latest",  # Change model here
    service_id="ollama-gemma3",
    async_client=ollama_client
)
```

### Memory System Configuration
The application uses Semantic Kernel's modern Vector Stores for conversation memory:

```python
# Memory record model with vector embeddings
@vectorstoremodel
@dataclass
class MemoryRecord:
    id: Annotated[str, VectorStoreField('key')]
    text: Annotated[str, VectorStoreField('data', is_full_text_indexed=True)]
    description: Annotated[str, VectorStoreField('data')]
    timestamp: Annotated[Optional[str], VectorStoreField('data')] = None

# Vector store collection
self.memory = InMemoryCollection(
    record_type=MemoryRecord,
    collection_name="ai_researcher_memory",
    embedding_generator=embeddings_service
)
```

## 🧪 Testing

### Test AI File Creation
```bash
python -c "
from ai_researcher_app import AIAssistant, FileManager
fm = FileManager()
ai = AIAssistant(fm)
import asyncio
result = asyncio.run(ai.process_request('Create a test file with hello world'))
print(result)
"
```

### Test Web Research
```bash
python -c "
import requests
response = requests.post('http://localhost:5001/api/research/web-search',
                        json={'query': 'artificial intelligence'})
print(response.json())
"
```

## 🔍 Troubleshooting

### Common Issues

#### Ollama Connection Failed
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
ollama serve

# Test model directly
ollama run gemma3:latest
```

#### Port Already in Use
```bash
# Kill process using port 5001
# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5001 | xargs kill -9
```

#### File Permission Errors
- Ensure the base directory path exists and is accessible
- Check write permissions for file operations
- The application is restricted to the configured base directory for security

## 📚 API Reference

### REST Endpoints

#### File Operations
- `GET /api/files` - List directory contents
- `GET /api/files/current-dir` - Get current directory
- `POST /api/files/change-dir` - Change directory
- `POST /api/files/read` - Read file content
- `POST /api/files/write` - Write content to file
- `POST /api/files/create-dir` - Create directory
- `POST /api/files/delete` - Delete file/directory
- `POST /api/files/open` - Open file in default application

#### AI Chat
- `POST /api/chat` - Send message to AI assistant
- `POST /api/chat/clear` - Clear conversation memory
- `GET /api/chat/memory` - Get conversation history

#### Web Research
- `POST /api/research/web-search` - Perform web search
- `POST /api/research/fetch-page` - Fetch webpage content

### WebSocket Events
- `file_operation_result` - File operation completion
- `chat_response` - AI chat response
- `status` - System status updates

## 🔒 Security Features

- **Directory Restrictions**: File operations limited to configured base directory
- **Path Validation**: All file paths validated against security boundaries
- **Input Sanitization**: User inputs validated and sanitized
- **Error Handling**: Graceful error handling without exposing system details

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- **Microsoft Semantic Kernel** - AI orchestration framework with modern Vector Stores
- **Semantic Kernel Vector Stores** - Advanced memory system with embeddings and vector search
- **Ollama** - Local AI model serving with embedding support
- **Flask** - Web framework
- **BeautifulSoup** - HTML parsing for web research
- **Bootstrap** - UI framework
- **DuckDuckGo** - Search engine for web research

---

**Happy researching with AI-powered tools! 🔬🤖**
