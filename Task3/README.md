# Web Scraper - Quick Start Guide

A general-purpose web scraper that extracts all types of data (text, images, links, tables) from any website with a beautiful modern UI.

## 🚀 How to Run

### Step 1: Install Dependencies (First Time Only)

```bash
# Navigate to project directory
cd /home/satyam/Desktop/Task3

# Create virtual environment (if not already created)
cd backend
python3 -m venv venv
cd ..

# Install Python packages
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### Step 2: Start the Backend Server

```bash
# From the Task3 directory
source backend/venv/bin/activate
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Step 3: Open the Frontend

Open your browser and navigate to:
```
file:///home/satyam/Desktop/Task3/frontend/index.html
```

Or simply double-click the `index.html` file in your file manager.

## 📖 How to Use

1. **Enter a URL** - Paste any website URL in the input field
2. **Click "Scrape Website"** - The scraper will fetch and extract all data
3. **View Results** - Browse through different tabs:
   - **Metadata** - Page title, description, keywords
   - **Headings** - All H1-H6 headings
   - **Paragraphs** - Text content
   - **Images** - All images with URLs
   - **Links** - Internal and external links
   - **Tables** - Structured table data

## 🎯 Example URLs to Try

- https://en.wikipedia.org/wiki/Web_scraping
- https://news.ycombinator.com/
- https://www.bbc.com/news
- Any website you want!

## 📁 Project Structure

```
Task3/
├── backend/
│   ├── main.py           # FastAPI server
│   ├── scraper.py        # Scraping logic
│   ├── requirements.txt  # Python dependencies
│   └── venv/            # Virtual environment
└── frontend/
    ├── index.html        # Main UI
    ├── style.css         # Styles
    └── script.js         # Frontend logic
```

## 🛑 To Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

## ✨ Features

- ✅ Extract all data types (text, images, links, tables)
- ✅ Beautiful modern dark UI with animations
- ✅ Organized results with tabbed interface
- ✅ Real-time statistics
- ✅ Works with any website
- ✅ Error handling and validation

## 🔧 Troubleshooting

**Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Backend not connecting:**
- Make sure the backend server is running on port 8000
- Check the browser console for errors (F12)

**No data extracted:**
- Some websites may block scrapers
- Check if the URL is valid and accessible

---

Built with Python, FastAPI, BeautifulSoup, and vanilla JavaScript.
