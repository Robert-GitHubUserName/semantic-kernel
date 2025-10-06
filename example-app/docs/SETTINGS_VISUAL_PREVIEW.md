# Settings Panel Visual Preview

## 🎨 Settings Button

```
┌────────────────────────────────────────────────────────┐
│                                           [⚙️ Settings] │
│  AI Researcher Application                              │
│                                                          │
└────────────────────────────────────────────────────────┘
```

**Location**: Fixed position, top-right corner  
**Style**: Blue gradient button with gear icon  
**Interaction**: Click to open settings modal  

---

## 📋 Settings Modal - Main View

```
╔═══════════════════════════════════════════════════════╗
║  ⚙️  AI Provider Settings                          ✕  ║
╠═══════════════════════════════════════════════════════╣
║                                                        ║
║  ┌──────────────────────────────────────────────┐   ║
║  │  🖥️  AI Provider                              │   ║
║  │  Select your preferred AI provider            │   ║
║  │                                                │   ║
║  │  ┌──────────────┐  ┌──────────────┐         │   ║
║  │  │  💻          │  │   🧠         │         │   ║
║  │  │              │  │              │         │   ║
║  │  │   Ollama     │  │   OpenAI     │         │   ║
║  │  │ Local Models │  │  ChatGPT API │         │   ║
║  │  │  [✓ Active]  │  │              │         │   ║
║  │  └──────────────┘  └──────────────┘         │   ║
║  └──────────────────────────────────────────────┘   ║
║                                                        ║
║  ┌──────────────────────────────────────────────┐   ║
║  │  🔌  Ollama Configuration                     │   ║
║  │                                                │   ║
║  │  Host URL                                      │   ║
║  │  [http://localhost:11434                   ]  │   ║
║  │  Ollama server address                        │   ║
║  │                                                │   ║
║  │  Model                                         │   ║
║  │  [gemma3:latest                            ]  │   ║
║  │  Ollama model name                            │   ║
║  │                                                │   ║
║  │  Embedding Model                               │   ║
║  │  [nomic-embed-text                         ]  │   ║
║  │  Model for text embeddings                    │   ║
║  └──────────────────────────────────────────────┘   ║
║                                                        ║
║  ┌──────────────────────────────────────────────┐   ║
║  │  🔌  Connection Status                        │   ║
║  │                                                │   ║
║  │  🟢  Connected to Ollama                      │   ║
║  │     http://localhost:11434         [🔄 Test] │   ║
║  └──────────────────────────────────────────────┘   ║
║                                                        ║
╠═══════════════════════════════════════════════════════╣
║            [↻ Reset]              [💾 Save Settings]  ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🔑 OpenAI Configuration View

```
╔═══════════════════════════════════════════════════════╗
║  ⚙️  AI Provider Settings                          ✕  ║
╠═══════════════════════════════════════════════════════╣
║                                                        ║
║  ┌──────────────────────────────────────────────┐   ║
║  │  🖥️  AI Provider                              │   ║
║  │                                                │   ║
║  │  ┌──────────────┐  ┌──────────────┐         │   ║
║  │  │  💻          │  │   🧠         │         │   ║
║  │  │   Ollama     │  │   OpenAI     │         │   ║
║  │  │ Local Models │  │  ChatGPT API │         │   ║
║  │  │              │  │  [✓ Active]  │         │   ║
║  │  └──────────────┘  └──────────────┘         │   ║
║  └──────────────────────────────────────────────┘   ║
║                                                        ║
║  ┌──────────────────────────────────────────────┐   ║
║  │  🔑  OpenAI Configuration                     │   ║
║  │                                                │   ║
║  │  API Key *                                     │   ║
║  │  [sk-•••••••••••••••••••••••••••••••     👁️]  │   ║
║  │  Get your key from platform.openai.com        │   ║
║  │                                                │   ║
║  │  Model                                         │   ║
║  │  [GPT-3.5 Turbo               ▼]             │   ║
║  │  Choose the OpenAI model to use               │   ║
║  │                                                │   ║
║  │  Base URL (Optional)                           │   ║
║  │  [https://api.openai.com/v1                ]  │   ║
║  │  Leave default unless using custom endpoint   │   ║
║  └──────────────────────────────────────────────┘   ║
║                                                        ║
║  ┌──────────────────────────────────────────────┐   ║
║  │  🔌  Connection Status                        │   ║
║  │                                                │   ║
║  │  🟢  API Key Configured                       │   ║
║  │     https://api.openai.com/v1     [🔄 Test]  │   ║
║  └──────────────────────────────────────────────┘   ║
║                                                        ║
╠═══════════════════════════════════════════════════════╣
║            [↻ Reset]              [💾 Save Settings]  ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🔄 Connection Status States

### ✅ Connected (Green)
```
┌──────────────────────────────────────────────┐
│  🟢  Connected to Ollama                     │
│     http://localhost:11434      [🔄 Test]   │
└──────────────────────────────────────────────┘
```

### ⏳ Testing (Orange)
```
┌──────────────────────────────────────────────┐
│  🟡  Testing connection...                   │
│     Please wait...              [🔄 Test]   │
└──────────────────────────────────────────────┘
```

### ❌ Disconnected (Red)
```
┌──────────────────────────────────────────────┐
│  🔴  Connection Failed                       │
│     Cannot connect to Ollama    [🔄 Test]   │
└──────────────────────────────────────────────┘
```

---

## 🎭 Provider Card States

### Active Card (Selected)
```
┌──────────────┐
│     🧠       │
│              │
│   OpenAI     │
│  ChatGPT API │
│  [✓ Active]  │  ← Blue border, highlighted
└──────────────┘
```

### Inactive Card (Not Selected)
```
┌──────────────┐
│     💻       │
│              │
│   Ollama     │
│ Local Models │
│              │  ← Gray border, normal
└──────────────┘
```

### Hover State
```
┌──────────────┐
│     💻       │  ← Slight elevation
│              │  ← Blue glow
│   Ollama     │
│ Local Models │
│              │
└──────────────┘
```

---

## 🎨 Color Palette

### Primary Colors
- **Button Blue**: #1e40af → #1e3a8a (gradient)
- **Success Green**: #10b981
- **Warning Orange**: #f59e0b
- **Error Red**: #ef4444

### Background Colors
- **Dark Primary**: #0f1419
- **Dark Secondary**: #1a2332
- **Border**: #2a3441
- **Input Background**: #1a2332

### Text Colors
- **Primary Text**: #e4e6ea
- **Secondary Text**: #9ca3af
- **Link Blue**: #60a5fa

---

## 📱 Responsive Behavior

### Desktop (> 768px)
```
┌────────────────────────────────────────┐
│  Full modal with side-by-side cards   │
│  Provider cards: 2 columns             │
│  All controls visible                  │
└────────────────────────────────────────┘
```

### Mobile (< 768px)
```
┌─────────────────────┐
│  Stacked layout     │
│  Provider cards:    │
│  1 column           │
│  Scrollable content │
└─────────────────────┘
```

---

## ✨ Animations

### Button Hover
```
Normal: [⚙️ Settings]
Hover:  [⚙️ Settings] ↑ (lifts up slightly with shadow)
```

### Connection Status Pulse
```
🟢 ← Pulsing animation (opacity 1.0 → 0.5 → 1.0)
```

### Provider Card Selection
```
Click → Blue border appears → Smooth transition (0.3s)
```

### Modal Open/Close
```
Open:  Fade in + scale up (backdrop darkens)
Close: Fade out + scale down
```

---

## 🖱️ Interactive Elements

### Clickable Areas
1. **⚙️ Settings Button** - Opens modal
2. **Provider Cards** - Selects provider
3. **👁️ Toggle Icon** - Shows/hides API key
4. **🔄 Test Button** - Tests connection
5. **↻ Reset Button** - Resets to defaults
6. **💾 Save Button** - Saves and reloads
7. **✕ Close Button** - Closes modal

### Keyboard Support
- **Tab** - Navigate between fields
- **Enter** - Submit forms
- **Esc** - Close modal (built-in Bootstrap)

---

## 📐 Layout Measurements

### Modal
- **Width**: 600px max
- **Border Radius**: 8px
- **Padding**: 20px sections
- **Gap**: 25px between sections

### Provider Cards
- **Width**: 48% each (2 columns with gap)
- **Height**: Auto
- **Border**: 2px solid
- **Border Radius**: 8px
- **Padding**: 15px

### Inputs
- **Height**: 40px
- **Border Radius**: 6px
- **Padding**: 10px 12px
- **Font Size**: 0.95rem

---

## 🎯 Focus States

All interactive elements have clear focus indicators:

```
Normal:  [Input Field              ]
Focus:   [Input Field              ] ← Blue glow
         ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
```

Accessibility compliant with WCAG 2.1 standards.
