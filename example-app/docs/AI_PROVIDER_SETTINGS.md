# AI Provider Settings Panel

## Overview
The AI Researcher application now includes a comprehensive settings panel that allows you to switch between different AI providers (OpenAI and Ollama) and configure their settings dynamically.

## Features

### 🎛️ Provider Selection
- **Ollama** - Local AI models (default)
- **OpenAI** - ChatGPT API integration

### ⚙️ Configuration Options

#### OpenAI Settings
- **API Key** - Secure input with show/hide toggle
- **Model Selection** - Choose from GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, etc.
- **Base URL** - Custom endpoint support for proxies or alternative APIs
- **Connection Testing** - Verify API key and connectivity

#### Ollama Settings
- **Host URL** - Configure Ollama server address (default: http://localhost:11434)
- **Model** - Specify the Ollama model to use (e.g., gemma3:latest, llama2, mistral)
- **Embedding Model** - Configure the model for text embeddings (default: nomic-embed-text)
- **Connection Testing** - Check Ollama server availability and model presence

### 🔌 Connection Status
- **Real-time Status Indicator** - Visual feedback on connection state
  - 🟢 Green - Connected
  - 🟡 Yellow - Testing
  - 🔴 Red - Disconnected
- **Test Connection** - Verify settings before saving
- **Detailed Messages** - Clear error messages and connection details

### 💾 Persistence
- **Local Storage** - Settings saved in browser for quick access
- **Server Storage** - Settings saved to `ai_provider_settings.json` file
- **Auto-reload** - Application restarts with new settings after save

## Usage

### Accessing Settings

1. Click the **Settings** button (gear icon) in the top-right corner
2. The settings modal will open

### Switching Providers

#### To Use OpenAI:
1. Click the **OpenAI** provider card
2. Enter your OpenAI API key (get one from [platform.openai.com](https://platform.openai.com/api-keys))
3. Select your preferred model
4. (Optional) Customize the base URL
5. Click **Test** to verify connection
6. Click **Save Settings**

#### To Use Ollama:
1. Click the **Ollama** provider card
2. Ensure Ollama is running locally or enter remote host URL
3. Specify the model name you want to use
4. Configure embedding model if needed
5. Click **Test** to verify connection
6. Click **Save Settings**

### Testing Connection

Before saving settings, you can test the connection:

1. Configure your provider settings
2. Click the **Test** button
3. Watch the connection status indicator:
   - Testing (yellow/orange)
   - Connected (green) - Ready to save
   - Failed (red) - Check your settings

### Saving Settings

1. Configure all necessary fields
2. Test the connection (recommended)
3. Click **Save Settings**
4. Confirm the success message
5. Application will reload with new settings

### Resetting to Defaults

To reset all settings to default values:

1. Open settings panel
2. Click **Reset to Default**
3. Confirm the action
4. Settings will revert to:
   - Provider: Ollama
   - Ollama Host: http://localhost:11434
   - Ollama Model: gemma3:latest
   - Embedding Model: nomic-embed-text

## API Endpoints

### POST `/api/settings/test-connection`
Test connection to AI provider

**Request Body:**
```json
{
  "provider": "ollama",
  "host_url": "http://localhost:11434",
  "model": "gemma3:latest"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Connected to Ollama - Model gemma3:latest available"
}
```

### POST `/api/settings/save`
Save AI provider settings

**Request Body:**
```json
{
  "provider": "openai",
  "openai": {
    "api_key": "sk-...",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-3.5-turbo"
  },
  "ollama": {
    "host_url": "http://localhost:11434",
    "model": "gemma3:latest",
    "embedding_model": "nomic-embed-text"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Settings saved successfully for openai"
}
```

### GET `/api/settings/load`
Load saved AI provider settings

**Response:**
```json
{
  "success": true,
  "settings": {
    "provider": "ollama",
    "ollama": { ... },
    "openai": { ... }
  }
}
```

## Configuration File

Settings are stored in `ai_provider_settings.json`:

```json
{
  "provider": "ollama",
  "ollama": {
    "host_url": "http://localhost:11434",
    "model": "gemma3:latest",
    "embedding_model": "nomic-embed-text"
  },
  "openai": {
    "api_key": "",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-3.5-turbo"
  }
}
```

## Security Notes

### API Key Storage
- **Browser**: API keys are stored in localStorage (client-side)
- **Server**: API keys are saved to `ai_provider_settings.json`
- **Recommendations**:
  - Do not commit `ai_provider_settings.json` to version control
  - Add `ai_provider_settings.json` to `.gitignore`
  - Use environment variables for production deployments
  - Rotate API keys regularly

### Best Practices
1. **Development**: Use Ollama (no API keys needed)
2. **Production**: Use environment variables for API keys
3. **Shared Environments**: Don't save API keys in the settings file
4. **Testing**: Always test connection before saving

## Styling

All styles are in `/static/css/style.css` under the section:
```css
/* ============================================
   Settings Panel Styles
   ============================================ */
```

Key classes:
- `.settings-button` - Floating settings button
- `.settings-modal` - Modal container
- `.provider-card` - Provider selection cards
- `.connection-status` - Connection indicator
- `.settings-section` - Section containers

## Troubleshooting

### OpenAI Connection Issues
- **Invalid API Key**: Check your key at platform.openai.com
- **Network Error**: Check internet connectivity
- **Rate Limit**: Verify your OpenAI account tier

### Ollama Connection Issues
- **Cannot Connect**: Ensure Ollama is running (`ollama serve`)
- **Model Not Found**: Pull the model first (`ollama pull gemma3:latest`)
- **Port Issues**: Check if port 11434 is available

### Settings Not Saving
- **Browser Storage**: Check if localStorage is enabled
- **File Permissions**: Ensure write permissions for `ai_provider_settings.json`
- **JSON Errors**: Verify settings file syntax

## Future Enhancements

Potential improvements:
- [ ] Support for additional providers (Anthropic, Cohere, etc.)
- [ ] Model auto-discovery
- [ ] API key encryption
- [ ] Multiple API key profiles
- [ ] Usage statistics and costs
- [ ] Model comparison tools
- [ ] Advanced model parameters (temperature, max tokens, etc.)

## Visual Design

### Color Scheme
- **Primary**: Blue gradient (#1e40af to #1e3a8a)
- **Success**: Green (#10b981)
- **Warning**: Orange/Yellow (#f59e0b)
- **Error**: Red (#ef4444)
- **Background**: Dark theme (#0f1419, #1a2332)

### Icons
- **Settings**: gear (fa-cog)
- **OpenAI**: brain (fa-brain)
- **Ollama**: laptop-code (fa-laptop-code)
- **Connection**: plug (fa-plug)
- **Test**: sync (fa-sync-alt)
- **Save**: save (fa-save)

## Keyboard Shortcuts

Future enhancement - potential shortcuts:
- `Ctrl/Cmd + ,` - Open settings
- `Esc` - Close settings
- `Ctrl/Cmd + S` - Save settings (within modal)
