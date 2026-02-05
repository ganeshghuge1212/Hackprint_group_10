# BEGINNER'S STEP-BY-STEP GUIDE
# Complete Setup Instructions for RAG System

## 🎯 What You'll Build

A smart HR assistant that can:
- Answer questions about employees
- Retrieve attendance data
- Explain company policies
- Provide leave information

All using AI and advanced search technology!

---

## 📚 STEP 1: Understanding the Prerequisites

### What You Need:

1. **A Computer with:**
   - Windows, Mac, or Linux
   - At least 4GB RAM (8GB better)
   - 5GB free disk space
   - Internet connection

2. **Basic Software:**
   - Python 3.8+ (Check: open terminal and type `python --version`)
   - Internet browser

3. **Accounts (All Free):**
   - Groq account for API key (we'll create this)

---

## 🚀 STEP 2: Install MongoDB (Database)

### Why? 
MongoDB stores your HR data (employees, attendance, leave records).

### How to Install:

#### **For Windows:**
1. Download MongoDB from: https://www.mongodb.com/try/download/community
2. Run the installer
3. Choose "Complete" installation
4. Check "Install MongoDB as a Service"
5. Click "Install"
6. Wait for installation to complete
7. **Verify:** Open Command Prompt and type `mongo --version`

#### **For Mac:**
```bash
# Open Terminal and run:
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB:
brew services start mongodb-community

# Verify:
mongo --version
```

#### **For Linux (Ubuntu/Debian):**
```bash
# Open Terminal and run:
sudo apt-get update
sudo apt-get install -y mongodb

# Start MongoDB:
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verify:
mongo --version
```

### ✅ Success Check:
You should see something like: `MongoDB shell version v4.4.x`

---

## 🔑 STEP 3: Get Your Groq API Key

### Why?
Groq provides fast AI (Gemma model) for generating answers.

### How to Get It:

1. **Go to:** https://console.groq.com
2. **Sign up** (it's free!)
   - Use your email
   - Verify email
3. **Create API Key:**
   - Click "API Keys" in the left menu
   - Click "Create API Key"
   - Copy the key (looks like: `gsk_...`)
   - Save it somewhere safe!

### ⚠️ Important:
- Free tier gives you plenty of requests for testing
- Don't share your API key
- Keep it secret!

---

## 💻 STEP 4: Setup Python Environment

### Install Python (if needed):
- **Windows:** https://www.python.org/downloads/
- **Mac:** Already installed or use `brew install python3`
- **Linux:** `sudo apt-get install python3 python3-pip`

### Create Project Directory:

**Windows:**
```cmd
cd C:\Users\YourName\Desktop
mkdir helix_rag_system
cd helix_rag_system
```

**Mac/Linux:**
```bash
cd ~/Desktop
mkdir helix_rag_system
cd helix_rag_system
```

### Create Virtual Environment:

**All Systems:**
```bash
# Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

**You should see `(venv)` in your terminal now!**

---

## 📦 STEP 5: Install Python Packages

### Copy all the Python files to your project directory

Then in your terminal:

```bash
# Make sure you're in the project directory and venv is activated
# You should see (venv) in your prompt

pip install -r requirements.txt
```

### ☕ Wait Time: 5-10 minutes
This downloads and installs:
- MongoDB driver
- AI models
- Math libraries
- Other tools

**Don't worry if you see yellow warnings - those are normal!**

---

## 📁 STEP 6: Prepare Your Data

### Create a data folder:

```bash
mkdir data
```

### Copy your data files into the `data/` folder:

Required files:
1. ✅ `employee_master.csv`
2. ✅ `attendance_logs_detailed.json`
3. ✅ `leave_intelligence.xlsx`
4. ⭕ `Helix_Pro_Policy_v2.pdf` (optional)

Your folder structure should look like:
```
helix_rag_system/
├── data/
│   ├── employee_master.csv
│   ├── attendance_logs_detailed.json
│   ├── leave_intelligence.xlsx
│   └── Helix_Pro_Policy_v2.pdf
├── config.py
├── ingest_data.py
├── query_interface.py
└── ... (other Python files)
```

---

## 🔐 STEP 7: Set Your API Key

### Save your Groq API key:

**Windows:**
```cmd
set GROQ_API_KEY=gsk_your_actual_key_here
```

**Mac/Linux:**
```bash
export GROQ_API_KEY=gsk_your_actual_key_here
```

### OR Create a .env file:

Create a file named `.env` in your project folder:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

---

## 🎬 STEP 8: Load the Data (First Time Only!)

### Run the ingestion script:

```bash
python ingest_data.py
```

### What Happens:
1. ✅ Reads your CSV, JSON, Excel files
2. ✅ Cleans and organizes data
3. ✅ Stores in MongoDB
4. ✅ Creates AI embeddings (converts text to numbers)
5. ✅ Builds FAISS indexes (for fast search)
6. ✅ Saves everything

### ⏱️ Wait Time: 2-5 minutes

### ✅ Success Looks Like:
```
============================================================
STEP 1: Loading Data from Files
============================================================
✓ Loaded CSV file
✓ Loaded JSON file
✓ Loaded Excel file

============================================================
STEP 2: Storing Data in MongoDB
============================================================
✓ Inserted 500 documents into employees
...

✅ DATA INGESTION COMPLETE!
```

---

## 🎮 STEP 9: Start Asking Questions!

### Run the query interface:

```bash
python query_interface.py
```

### Try These Questions:

1. "Who is employee EMP1005?"
2. "List employees in Engineering"
3. "What is the leave policy?"
4. "Show attendance for EMP1001"
5. "What happens if I miss check-out 5 times?"

### Example Interaction:
```
💬 Your Query: Who is employee EMP1005?

======================================================================
📝 ANSWER:
======================================================================
Employee EMP1005 is Calvin Nielsen, working in Marketing at the 
Bangalore location. He joined on April 20, 2024...

📊 Confidence: 95% (high)
🔍 Search Method: structured
======================================================================
```

---

## 🎯 STEP 10: Understanding How It Works

### Behind the Scenes:

1. **You ask a question** → "Who is employee EMP1005?"

2. **System decides approach:**
   - If specific ID → Query MongoDB directly ✅
   - If general question → Use AI search

3. **AI Search Process:**
   - Convert your question to numbers (embedding)
   - Find similar data in FAISS index
   - Retrieve relevant documents

4. **Generate Answer:**
   - Send question + documents to Gemma AI
   - AI writes a natural answer
   - Add confidence score and sources

5. **Show you the result!**

---

## 🔧 Common Issues & Solutions

### ❌ "MongoDB connection failed"
**Solution:**
```bash
# Check if MongoDB is running
# Windows:
net start MongoDB

# Mac:
brew services start mongodb-community

# Linux:
sudo systemctl start mongodb
```

### ❌ "GROQ_API_KEY not set"
**Solution:**
- Re-run the export/set command
- Or create .env file with your key
- Make sure there are no spaces or quotes

### ❌ "No module named 'pymongo'"
**Solution:**
```bash
# Make sure venv is activated (you see (venv))
# Then reinstall:
pip install -r requirements.txt
```

### ❌ "No data found in database"
**Solution:**
```bash
# Run ingestion again:
python ingest_data.py
```

---

## 📊 What Each File Does

**Simple Explanation:**

- `config.py` → Settings (like a control panel)
- `database_handler.py` → Talks to MongoDB
- `data_loader.py` → Reads your files
- `embedding_generator.py` → Converts text to numbers for AI
- `faiss_vector_store.py` → Fast search engine
- `llm_interface.py` → Talks to Gemma AI
- `rag_system.py` → Main brain (coordinates everything)
- `ingest_data.py` → One-time data loading
- `query_interface.py` → Where you ask questions

---

## 🎓 Next Steps

### Experiment:
1. Ask different questions
2. Try combining multiple queries
3. Ask about policies, employees, attendance

### Customize:
1. Edit `config.py` to change settings
2. Add more data files
3. Adjust similarity thresholds

### Learn More:
- Read the comments in each Python file
- Try modifying simple things
- Google terms you don't understand

---

## 🆘 Getting Help

### If Stuck:

1. **Read error messages carefully**
   - They often tell you exactly what's wrong

2. **Check the logs**
   - Terminal output shows what happened

3. **Verify each step**
   - Is MongoDB running?
   - Is venv activated?
   - Are files in the right place?

4. **Start fresh**
   - Delete and recreate venv
   - Re-run ingestion
   - Check API key

---

## ✅ Success Checklist

Before asking questions, verify:

- [ ] MongoDB is installed and running
- [ ] Python virtual environment is activated
- [ ] All packages installed (`pip list` shows pymongo, faiss-cpu, etc.)
- [ ] Groq API key is set
- [ ] Data files are in `data/` folder
- [ ] Ingestion completed successfully (✅ messages)
- [ ] FAISS indexes created (check `faiss_indexes/` folder)

---

## 🎉 Congratulations!

You've built a production-grade RAG system!

**You now have:**
- ✅ AI-powered HR assistant
- ✅ Fast semantic search
- ✅ Natural language interface
- ✅ Source attribution
- ✅ Confidence scoring

**Keep exploring and learning! 🚀**
