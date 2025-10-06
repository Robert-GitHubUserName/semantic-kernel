# Settings Panel - Quick Reference Card

## 🚀 Quick Start

### Open Settings
Click the **⚙️ Settings** button in the top-right corner

### Switch to OpenAI
1. Click **OpenAI** card
2. Enter API key from [platform.openai.com](https://platform.openai.com/api-keys)
3. Select model (GPT-3.5 Turbo, GPT-4, etc.)
4. Click **Test** to verify
5. Click **Save Settings**

### Switch to Ollama
1. Click **Ollama** card
2. Verify host URL (default: http://localhost:11434)
3. Enter model name (gemma3:latest, llama2, mistral, etc.)
4. Click **Test** to verify
5. Click **Save Settings**

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Provider Cards** | Visual selection between Ollama & OpenAI |
| **API Key Toggle** | Show/hide sensitive data with 👁️ icon |
| **Connection Test** | Verify settings before saving |
| **Status Indicator** | 🟢 Connected / 🟡 Testing / 🔴 Error |
| **Auto-save** | Settings persist in browser & server |
| **Reset** | Restore default settings anytime |

---

## 📋 Default Settings

### Ollama
- **Host**: http://localhost:11434
- **Model**: gemma3:latest
- **Embeddings**: nomic-embed-text

### OpenAI
- **Base URL**: https://api.openai.com/v1
- **Model**: gpt-3.5-turbo
- **API Key**: (required - enter your own)

---

## 🔧 API Endpoints

```
POST /api/settings/test-connection  - Test provider
POST /api/settings/save             - Save settings
GET  /api/settings/load             - Load settings
```

---

## 🛡️ Security Tips

✅ **Never commit** `ai_provider_settings.json` to git  
✅ **Use environment variables** in production  
✅ **Rotate API keys** regularly  
✅ **Test connection** before saving  

---

## 🐛 Troubleshooting

### Ollama Won't Connect
```bash
# Check if Ollama is running
ollama serve

# Pull a model if needed
ollama pull gemma3:latest
```

### OpenAI Connection Failed
- Verify API key at platform.openai.com
- Check internet connection
- Ensure billing is set up

### Settings Not Saving
- Check browser localStorage is enabled
- Verify file write permissions
- Look for console errors (F12)

---

## 💡 Pro Tips

1. **Test First** - Always test connection before saving
2. **Use Ollama for Dev** - No API costs, runs locally
3. **Custom Endpoints** - Configure proxies via Base URL
4. **Model Selection** - Choose based on task complexity
5. **Keep Defaults** - Reset button restores working config

---

## 📞 Support

- **Documentation**: See `AI_PROVIDER_SETTINGS.md`
- **Issues**: Check console (F12) for errors
- **Models**: [Ollama Library](https://ollama.com/library)
- **OpenAI**: [API Documentation](https://platform.openai.com/docs)
