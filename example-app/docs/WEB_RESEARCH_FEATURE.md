# Web Research Document Creation Feature

## Overview
The AI Researcher application now supports comprehensive document creation from web research, including:
- **Web scraping** using BeautifulSoup
- **Screenshot capture** using Playwright
- **Automatic document generation** with content and images

## New Features

### 1. Web Page Scraping (`scrape_webpage`)
Extracts clean, readable content from web pages:
- Removes scripts and styling
- Extracts main content areas
- Includes page title
- Formats content for readability

### 2. Screenshot Capture (`take_webpage_screenshot`)
Captures full-page screenshots using Playwright:
- High-resolution screenshots (1920x1080 viewport)
- Full-page capture (scrolling)
- Headless browser automation
- Screenshots saved to `data` folder

### 3. Document Creation (`create_document_from_web`)
Creates comprehensive Markdown documents from multiple URLs:
- Scrapes content from each URL
- Captures screenshot of each page
- Combines content into a single document
- Embeds screenshots with proper linking
- Generates professional formatting

## API Endpoint

### Create Research Document
**Endpoint:** `POST /api/research/create-document`

**Request Body:**
```json
{
  "urls": [
    "https://example.com",
    "https://www.wikipedia.org"
  ],
  "title": "My Research Document"
}
```

**Response:**
```json
{
  "success": true,
  "document_path": "C:\\path\\to\\document.md",
  "filename": "My_Research_Document.md",
  "screenshots": [
    "My_Research_Document_source_1.png",
    "My_Research_Document_source_2.png"
  ],
  "urls_processed": 2,
  "message": "Document created successfully with 2 screenshots"
}
```

## Usage Examples

### Python Example
```python
import requests

response = requests.post(
    "http://localhost:5001/api/research/create-document",
    json={
        "urls": ["https://example.com"],
        "title": "Example Research"
    }
)
print(response.json())
```

### JavaScript/Fetch Example
```javascript
fetch('http://localhost:5001/api/research/create-document', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    urls: ['https://example.com'],
    title: 'Example Research'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL Example
```bash
curl -X POST http://localhost:5001/api/research/create-document \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com"],
    "title": "Example Research"
  }'
```

## Document Structure

The generated Markdown document includes:

```markdown
# [Title]

Generated on: 2025-10-05 14:30:00
Source URLs: https://example.com, ...

---

## Source 1: https://example.com

### Title: Example Page

### Content:
[Scraped and formatted content]

### Screenshot: filename.png
![Screenshot 1](data/filename.png)

---
```

## File Storage

- **Documents**: Saved to current working directory
- **Screenshots**: Saved to `example-app/data/` folder
- **Format**: 
  - Documents: Markdown (`.md`)
  - Screenshots: PNG (`.png`)

## Dependencies

### Required Packages
- `playwright>=1.40.0` - Browser automation for screenshots
- `beautifulsoup4>=4.12.0` - HTML parsing for web scraping
- `requests>=2.31.0` - HTTP requests

### Installation
```bash
pip install playwright beautifulsoup4 requests
playwright install chromium
```

## Technical Details

### Browser Configuration
- **Browser**: Chromium (headless)
- **Viewport**: 1920x1080
- **User Agent**: Modern Chrome
- **Wait Strategy**: Network idle + 2s delay

### Content Extraction
- Prioritizes main content areas (`<main>`, `<article>`, etc.)
- Removes navigation, scripts, and styling
- Limits content to 100 lines for readability
- Preserves formatting with proper line breaks

### Error Handling
- Graceful fallback if scraping fails
- Continues processing remaining URLs on error
- Reports errors in generated document
- Safe error messages for missing dependencies

## Testing

Run the test script:
```bash
cd example-app
python test_document_creation.py
```

This will:
1. Create a test document from example URLs
2. Capture screenshots of the pages
3. Save everything to the current directory
4. Display results in the console

## Future Enhancements

Potential improvements:
- [ ] Support for PDF export
- [ ] Custom screenshot dimensions
- [ ] Selective element screenshots
- [ ] Multiple browser engines
- [ ] Async/batch processing
- [ ] Content summarization with AI
- [ ] Citation formatting
- [ ] Table of contents generation
