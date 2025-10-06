# Ollama Model Dropdown Feature

## 📋 Overview

The AI Researcher application now features **dynamic model selection** for Ollama providers. Instead of manually typing model names, you can now browse and select from your locally available Ollama models using convenient dropdown menus.

## ✨ Features

### 1. **Dynamic Model Discovery**
- Automatically fetches available models from your Ollama instance
- Real-time model list updates via API
- Separate dropdowns for chat models and embedding models

### 2. **Smart Filtering**
- **Chat Models**: Shows all available models
- **Embedding Models**: Intelligently filters for embedding-specific models (containing 'embed', 'nomic', 'mxbai')
- Falls back to showing all models if no embedding models found

### 3. **User-Friendly Interface**
- 🔄 Refresh buttons next to each dropdown
- Visual loading indicators (spinning icon)
- Toast notifications for success/error feedback
- Preserves your selection when refreshing

### 4. **Auto-Loading**
- Models load automatically when:
  - Opening the settings modal (if Ollama is selected)
  - Switching to the Ollama provider
  - Clicking the refresh button

## 🎯 How to Use

### Step 1: Open Settings
Click the **⚙️ Settings** button in the top-right corner of the application.

### Step 2: Select Ollama Provider
If not already selected, click on the **Ollama** provider card.

### Step 3: View Available Models
The dropdowns will automatically populate with your available models:

```
┌────────────────────────────────────────┐
│ Model                          [🔄]    │
│ ┌────────────────────────────────────┐ │
│ │ llama2:latest                   ▼ │ │
│ ├────────────────────────────────────┤ │
│ │ mistral:latest                     │ │
│ │ gemma3:latest                      │ │
│ │ codellama:latest                   │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

### Step 4: Select Your Model
Click on the dropdown and choose your desired model from the list.

### Step 5: Refresh Models (Optional)
If you've recently pulled new models, click the **🔄** refresh button to update the list.

## 🔧 Technical Details

### API Endpoint

**POST** `/api/ollama/models`

**Request Body:**
```json
{
  "host_url": "http://localhost:11434"
}
```

**Response (Success):**
```json
{
  "success": true,
  "models": [
    "llama2:latest",
    "mistral:latest",
    "gemma3:latest",
    "nomic-embed-text:latest"
  ],
  "count": 4
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Cannot connect to Ollama. Please check the host URL."
}
```

### Frontend Functions

#### `refreshOllamaModels()`
Fetches and populates the chat model dropdown.

```javascript
async function refreshOllamaModels() {
    // Fetches models from Ollama API
    // Populates the dropdown with results
    // Shows toast notification
    // Preserves current selection if available
}
```

#### `refreshOllamaEmbeddingModels()`
Fetches and populates the embedding model dropdown with intelligent filtering.

```javascript
async function refreshOllamaEmbeddingModels() {
    // Fetches all models
    // Filters for embedding models
    // Falls back to all models if no matches
    // Updates dropdown and shows notification
}
```

### Model Filtering Logic

**Embedding Model Detection:**
```javascript
const embeddingModels = result.models.filter(model => 
    model.toLowerCase().includes('embed') || 
    model.toLowerCase().includes('nomic') ||
    model.toLowerCase().includes('mxbai')
);
```

## 🎨 UI Components

### Refresh Button
```html
<button type="button" 
        class="btn btn-sm btn-outline-primary ms-2" 
        onclick="refreshOllamaModels()" 
        title="Refresh models list">
    <i class="fas fa-sync-alt"></i>
</button>
```

**Styling:**
- Blue outline style
- Hover effect with background fill
- Disabled state while loading
- Spinning animation during API call

### Model Dropdown
```html
<select id="ollama-model" class="form-control">
    <option value="gemma3:latest">gemma3:latest</option>
    <!-- Populated dynamically -->
</select>
```

### Toast Notifications
```javascript
showToast('Found 5 Ollama models', 'success');
showToast('Failed to fetch models', 'error');
```

**Notification Types:**
- 🟢 **Success**: Green background (`#10b981`)
- 🔴 **Error**: Red background (`#ef4444`)
- 🔵 **Info**: Blue background (`#3b82f6`)

**Duration**: 3 seconds with slide-in/out animation

## 📊 State Management

### Loading State
```javascript
// Show loading
icon.classList.add('fa-spin');
refreshBtn.disabled = true;

// Hide loading
icon.classList.remove('fa-spin');
refreshBtn.disabled = false;
```

### Selection Preservation
```javascript
// Save current selection
const currentModel = modelSelect.value;

// Restore after refresh
if (currentModel && result.models.includes(currentModel)) {
    modelSelect.value = currentModel;
}
```

## 🚨 Error Handling

### Connection Timeout
```
Error: Connection timeout. Is Ollama running?
Status Code: 400
```

### Connection Refused
```
Error: Cannot connect to Ollama. Please check the host URL.
Status Code: 400
```

### No Models Found
```
Error: No models found
Behavior: Keeps default model in dropdown
```

### API Error
```
Error: Failed to fetch models. Status code: [code]
Behavior: Shows toast notification, preserves dropdown
```

## 🎯 Best Practices

### 1. **Check Ollama Status**
Ensure Ollama is running before refreshing models:
```bash
ollama list
```

### 2. **Use Appropriate Models**
- **Chat Models**: General-purpose models (llama2, mistral, gemma3)
- **Embedding Models**: Specialized models (nomic-embed-text, mxbai-embed-large)

### 3. **Network Configuration**
If using a custom Ollama host, update the **Host URL** field before refreshing:
```
Default: http://localhost:11434
Custom:  http://192.168.1.100:11434
```

### 4. **Model Availability**
Pull models before they appear in the dropdown:
```bash
ollama pull llama2
ollama pull nomic-embed-text
```

## 🐛 Troubleshooting

### Issue: No models appear in dropdown
**Solutions:**
1. Check if Ollama is running: `ollama list`
2. Verify host URL is correct
3. Click the refresh button manually
4. Check browser console for errors

### Issue: Refresh button not working
**Solutions:**
1. Check network connectivity
2. Verify Ollama API is accessible
3. Look for JavaScript errors in console
4. Try reloading the page

### Issue: Old model selection lost after refresh
**Solution:** This is expected behavior when the model is no longer available. The dropdown defaults to the first available model.

### Issue: Embedding models not filtered correctly
**Solution:** The filter looks for 'embed', 'nomic', or 'mxbai' in model names. If your embedding model has a different name, it will appear in the "all models" fallback list.

## 🔄 Auto-Refresh Triggers

The model dropdowns automatically refresh in these scenarios:

1. **Opening Settings Modal** (when Ollama is selected)
   ```javascript
   openSettings() → refreshOllamaModels() + refreshOllamaEmbeddingModels()
   ```

2. **Switching to Ollama Provider**
   ```javascript
   selectProvider('ollama') → refreshOllamaModels() + refreshOllamaEmbeddingModels()
   ```

3. **Manual Refresh Button Click**
   ```javascript
   <button onclick="refreshOllamaModels()">
   ```

## 📈 Performance Considerations

- **API Timeout**: 5 seconds
- **Parallel Requests**: Model and embedding model fetches run independently
- **Caching**: No caching; always fetches fresh data
- **Debouncing**: Not implemented (manual refresh only)

## 🎨 Visual Feedback

### Loading State
```
┌────────────────────────────────┐
│ Model              [🔄 ↻]     │  ← Spinning icon
│                     (disabled)  │
└────────────────────────────────┘
```

### Success State
```
┌──────────────────────────────────┐
│ 🟢 Found 5 Ollama models         │  ← Green toast
└──────────────────────────────────┘
```

### Error State
```
┌──────────────────────────────────┐
│ 🔴 Failed to fetch models        │  ← Red toast
└──────────────────────────────────┘
```

## 🔐 Security Notes

- No authentication required (local Ollama instance)
- Host URL validation on backend
- Timeout protection against hanging requests
- Error messages don't expose sensitive information

## 🚀 Future Enhancements

Potential improvements for future versions:

1. **Model Metadata Display**
   - Show model size
   - Display last modified date
   - Indicate model family (Llama, Mistral, etc.)

2. **Search/Filter**
   - Search box for filtering models by name
   - Group models by family or size
   - Favorite models feature

3. **Model Management**
   - Pull models directly from UI
   - Delete unused models
   - Update existing models

4. **Performance**
   - Cache model list for 60 seconds
   - Debounce refresh requests
   - Show model count before fetching

5. **Advanced Filtering**
   - Filter by model size
   - Filter by quantization level
   - Show only compatible models

## 📚 Related Documentation

- [AI Provider Settings](AI_PROVIDER_SETTINGS.md)
- [Settings Implementation Summary](SETTINGS_IMPLEMENTATION_SUMMARY.md)
- [Settings Quick Reference](SETTINGS_QUICK_REFERENCE.md)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)

## 🎉 Summary

The Ollama model dropdown feature provides a **user-friendly, dynamic way to select AI models** without memorizing or typing model names. With automatic discovery, smart filtering, and clear visual feedback, managing Ollama models is now easier than ever!

**Key Benefits:**
- ✅ No manual typing required
- ✅ Always up-to-date model list
- ✅ Smart filtering for embedding models
- ✅ Clear error messages and feedback
- ✅ Seamless integration with existing settings
