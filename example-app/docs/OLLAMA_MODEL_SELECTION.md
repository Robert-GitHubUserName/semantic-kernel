# Dynamic Ollama Model Selection Feature

## 📋 Overview

The AI Researcher App now features **dynamic model selection** for Ollama, allowing users to automatically fetch and select from available models instead of manually typing model names.

## ✨ New Features

### 1. **Dynamic Model Dropdown**
- Replaces text input with a searchable dropdown
- Automatically populated with models from your Ollama instance
- Applies to both **Chat Models** and **Embedding Models**

### 2. **Refresh Buttons**
- Manual refresh capability with spinning animation
- Instant feedback on model availability
- Updates dropdown without page reload

### 3. **Auto-Refresh on Provider Selection**
- Models automatically load when opening settings
- Updates when switching to Ollama provider
- Ensures up-to-date model list

### 4. **Smart Filtering**
- **Embedding Models**: Automatically filters for embedding-specific models
  - Looks for models containing: `embed`, `nomic`, `mxbai`
  - Falls back to all models if no embedding models found

### 5. **Toast Notifications**
- Visual feedback for model refresh operations
- Success/error notifications with slide-in animation
- Auto-dismisses after 3 seconds

## 🎯 How to Use

### Basic Usage

1. **Open Settings** - Click the ⚙️ settings button (top-right)
2. **Select Ollama Provider** - Models auto-refresh
3. **Choose Models** - Select from dropdown lists
4. **Manual Refresh** - Click 🔄 button next to any dropdown

### Model Selection Flow

```
Settings Button → Settings Modal → Ollama Selected
    ↓
Auto-refresh models from Ollama API
    ↓
Dropdowns populated with available models
    ↓
Select preferred chat & embedding models
    ↓
Save Settings
```

## 🔧 Technical Details

### New API Endpoint

**`POST /api/ollama/models`**

Fetches available models from Ollama instance.

**Request:**
```json
{
  "host_url": "http://localhost:11434"
}
```

**Response:**
```json
{
  "success": true,
  "models": [
    "gemma3:latest",
    "llama2:latest",
    "nomic-embed-text",
    "mistral:latest"
  ],
  "count": 4
}
```

### JavaScript Functions

#### `refreshOllamaModels()`
Fetches and populates the chat model dropdown.

**Features:**
- Preserves current selection if still available
- Shows loading spinner during fetch
- Handles connection errors gracefully
- Sorts models alphabetically

#### `refreshOllamaEmbeddingModels()`
Fetches and populates the embedding model dropdown.

**Features:**
- Filters for embedding-specific models
- Falls back to all models if no embedding models found
- Same error handling as chat models
- Prioritizes models with "embed" in name

### UI Changes

#### Before (Text Input):
```html
<input type="text" id="ollama-model" placeholder="gemma3:latest">
```

#### After (Dropdown + Refresh):
```html
<label>
  Model
  <button onclick="refreshOllamaModels()">
    <i class="fas fa-sync-alt"></i>
  </button>
</label>
<select id="ollama-model">
  <option value="gemma3:latest">gemma3:latest</option>
  <option value="llama2:latest">llama2:latest</option>
  <!-- More options populated dynamically -->
</select>
```

## 🎨 Visual Enhancements

### Refresh Button
- **Style**: Blue outline button with sync icon
- **Hover**: Transforms to filled blue background
- **Active**: Spinning animation while fetching
- **Disabled**: Grayed out during operation

### Toast Notifications
- **Position**: Top-right (below settings button)
- **Colors**: 
  - Success: Green (#10b981)
  - Error: Red (#ef4444)
  - Info: Blue (#3b82f6)
- **Animation**: Slide in from right, fade out
- **Duration**: 3 seconds

### Dropdown Styling
- **Theme**: Dark background with light text
- **Border**: Subtle border with focus highlight
- **Options**: Full-width, easy to read
- **Scroll**: Custom scrollbar on overflow

## 📊 Model Detection

### Embedding Model Filter Logic

```javascript
const embeddingModels = result.models.filter(model => 
    model.toLowerCase().includes('embed') || 
    model.toLowerCase().includes('nomic') ||
    model.toLowerCase().includes('mxbai')
);
```

**Common Embedding Models:**
- `nomic-embed-text`
- `mxbai-embed-large`
- `all-minilm`
- Any model with "embed" in the name

## 🔄 Auto-Refresh Triggers

Models are automatically refreshed in these scenarios:

1. **Settings Modal Opens** (if Ollama selected)
   ```javascript
   function openSettings() {
       if (currentProvider === 'ollama') {
           refreshOllamaModels();
           refreshOllamaEmbeddingModels();
       }
   }
   ```

2. **Ollama Provider Selected**
   ```javascript
   function selectProvider('ollama') {
       // ... show Ollama config
       refreshOllamaModels();
       refreshOllamaEmbeddingModels();
   }
   ```

3. **Manual Refresh Button Clicked**
   - User clicks 🔄 button next to dropdown
   - Manually triggers refresh on demand

## ⚠️ Error Handling

### Connection Timeout
```
Error: Connection timeout. Is Ollama running?
Action: Start Ollama service
```

### Connection Refused
```
Error: Cannot connect to Ollama. Please check the host URL.
Action: Verify host URL in settings
```

### No Models Found
```
Error: No models found
Action: 
- Check if Ollama has models installed
- Run: ollama pull gemma3:latest
```

### Fallback Behavior
If API call fails, dropdown retains current selection with at least one option.

## 🚀 Benefits

### For Users
- ✅ **No more typos** - Select from verified available models
- ✅ **Discover models** - See all installed models at a glance
- ✅ **Instant validation** - Only shows models that exist
- ✅ **Better UX** - Visual feedback and clear selections

### For Developers
- ✅ **Reduced errors** - Prevents invalid model names
- ✅ **API integration** - Leverages Ollama's `/api/tags` endpoint
- ✅ **Maintainable** - Easy to extend to other providers
- ✅ **Error handling** - Comprehensive error scenarios covered

## 🔮 Future Enhancements

### Potential Improvements
1. **Model Details** - Show model size, family, and capabilities
2. **Model Parameters** - Configure temperature, context length per model
3. **Model Tags** - Filter by tags (latest, specific versions)
4. **Model Search** - Search/filter within dropdown for large lists
5. **Model Metadata** - Display last used, performance metrics
6. **Auto-Update** - Periodic background refresh of model list
7. **Model Recommendations** - Suggest best models for task type

### Additional Features
- Model download progress tracking
- Model pull integration (download new models from UI)
- Model performance comparison
- Custom model aliases

## 📝 Code Files Modified

### Backend
- **`ai_researcher_app.py`** - Added `/api/ollama/models` endpoint

### Frontend
- **`templates/ai_researcher.html`** - Updated form controls, added JavaScript functions
- **`static/css/style.css`** - Added toast animations and button styling

### Documentation
- **`docs/OLLAMA_MODEL_SELECTION.md`** - This document

## 🧪 Testing Checklist

- [ ] Ollama running locally
- [ ] Settings button opens modal
- [ ] Model dropdown populated automatically
- [ ] Refresh button triggers model reload
- [ ] Spinning animation shows during load
- [ ] Toast notification appears on success/error
- [ ] Selected model persists after refresh
- [ ] Embedding models filtered correctly
- [ ] Error handling works when Ollama offline
- [ ] Settings save with selected models
- [ ] Page reload restores model selections

## 📞 Support

### Common Issues

**Q: Dropdown shows only one model?**  
A: Click the 🔄 refresh button to reload models from Ollama.

**Q: No models appear?**  
A: Ensure Ollama is running and accessible at the configured host URL.

**Q: Can't find my model?**  
A: Check that the model is installed: `ollama list`

**Q: Refresh button not working?**  
A: Check browser console for errors and verify Ollama API is accessible.

---

## 📅 Version History

- **v1.1.0** (October 5, 2025) - Initial dynamic model selection feature
  - Added model dropdown for chat models
  - Added model dropdown for embedding models
  - Implemented auto-refresh on provider selection
  - Added manual refresh buttons
  - Implemented toast notifications
  - Added embedding model filtering

---

*For more information, see [AI_PROVIDER_SETTINGS.md](AI_PROVIDER_SETTINGS.md)*
