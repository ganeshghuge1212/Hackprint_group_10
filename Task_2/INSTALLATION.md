# INSTALLATION GUIDE

## 🎯 Complete Setup Instructions

This guide will walk you through setting up the Helix HR RAG System from scratch.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Step-by-Step Installation](#step-by-step-installation)
4. [Verification](#verification)
5. [First Query](#first-query)
6. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements:
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB (8GB recommended)
- **Disk**: 5GB free space
- **CPU**: Any modern processor
- **Internet**: Required for installation and API calls

### Software Requirements:
- Python 3.8 or higher
- MongoDB 4.4 or higher
- pip (Python package manager)
- git (optional, for version control)

---

## ✅ Pre-Installation Checklist

Before starting, ensure you have:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] MongoDB installed (see below)
- [ ] Groq API key (get free at https://console.groq.com)
- [ ] Your data files ready:
  - [ ] employee_master.csv
  - [ ] attendance_logs_detailed.json
  - [ ] leave_intelligence.xlsx
  - [ ] Helix_Pro_Policy_v2.pdf (optional)

---

## 🚀 Step-by-Step Installation

### STEP 1: Install MongoDB

#### **Windows:**
1. Download MongoDB Community Server from:
   https://www.mongodb.com/try/download/community

2. Run the installer (`.msi` file)

3. During installation:
   - Select "Complete" setup
   - Check "Install MongoDB as a Service"
   - Use default port: 27017

4. Verify installation:
   ```cmd
   mongo --version
   ```

#### **macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Verify
mongo --version
```

#### **Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb

# Start service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verify
mongo --version
```

**Expected Output:**
```
MongoDB shell version v4.4.x
```

---

### STEP 2: Create Project Directory

#### **Windows:**
```cmd
cd C:\Users\%USERNAME%\Desktop
mkdir helix_rag_system
cd helix_rag_system
```

#### **macOS/Linux:**
```bash
cd ~/Desktop
mkdir helix_rag_system
cd helix_rag_system
```

---

### STEP 3: Copy Project Files

1. **Extract/Download** all project files to the `helix_rag_system` directory

2. **Verify** you have these files:
   ```
   helix_rag_system/
   ├── config.py
   ├── database_handler.py
   ├── data_loader.py
   ├── embedding_generator.py
   ├── faiss_vector_store.py
   ├── llm_interface.py
   ├── rag_system.py
   ├── ingest_data.py
   ├── query_interface.py
   ├── examples.py
   ├── demo_standalone.py
   ├── requirements.txt
   ├── setup.sh
   ├── README.md
   ├── BEGINNER_GUIDE.md
   └── PROJECT_SUMMARY.md
   ```

---

### STEP 4: Setup Python Virtual Environment

#### **All Systems:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

**You should see `(venv)` in your terminal prompt**

---

### STEP 5: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**⏱️ This will take 5-10 minutes**

The installation downloads:
- MongoDB driver (pymongo)
- FAISS library (~200MB)
- PyTorch (~700MB)
- Sentence Transformers (~400MB)
- Other dependencies

**Note:** You may see some yellow warnings - these are normal!

---

### STEP 6: Get Groq API Key

1. **Visit**: https://console.groq.com

2. **Sign Up** (free):
   - Click "Sign Up"
   - Enter your email
   - Verify email address

3. **Create API Key**:
   - After login, click "API Keys" in sidebar
   - Click "Create API Key"
   - Name it: "Helix RAG System"
   - Copy the key (starts with `gsk_`)

4. **Save the key** somewhere safe!

---

### STEP 7: Configure API Key

#### **Option A: Environment Variable (Recommended)**

**Windows:**
```cmd
set GROQ_API_KEY=gsk_your_actual_key_here
```

**macOS/Linux:**
```bash
export GROQ_API_KEY=gsk_your_actual_key_here
```

**Note:** You'll need to set this each time you open a new terminal.

#### **Option B: Create .env File**

Create a file named `.env` in the project directory:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

#### **Option C: Modify config.py**

Edit `config.py` and add:
```python
GROQ_API_KEY = "gsk_your_actual_key_here"
```

**⚠️ Don't commit this file to version control!**

---

### STEP 8: Prepare Data Files

1. **Create data directory**:
   ```bash
   mkdir data
   ```

2. **Copy your files** into `data/`:
   ```
   data/
   ├── employee_master.csv
   ├── attendance_logs_detailed.json
   ├── leave_intelligence.xlsx
   └── Helix_Pro_Policy_v2.pdf (optional)
   ```

3. **Verify files**:
   ```bash
   # Windows:
   dir data

   # macOS/Linux:
   ls -l data/
   ```

---

### STEP 9: Load Data (One-Time Setup)

Run the data ingestion script:

```bash
python ingest_data.py
```

**What happens:**
1. ✅ Connects to MongoDB
2. ✅ Loads CSV, JSON, Excel files
3. ✅ Cleans and normalizes data
4. ✅ Generates AI embeddings
5. ✅ Creates FAISS indexes
6. ✅ Saves indexes to disk

**⏱️ Expected Time: 2-5 minutes**

**Expected Output:**
```
============================================================
  HELIX HR RAG SYSTEM - DATA INGESTION
============================================================

🚀 Initializing RAG System...
✓ Connected to MongoDB database: helix_hr_rag
✓ Loaded embedding model on cpu
  Embedding dimension: 384

============================================================
STEP 1: Loading Data from Files
============================================================

[1/4] Loading Employee Data...
✓ Loaded CSV file: data/employee_master.csv
  Rows: 500, Columns: 12
  
... (more output) ...

============================================================
✅ DATA INGESTION COMPLETE!
============================================================

📊 DATA SUMMARY:
  Employees: 500
  Attendance Records: 32500
  Leave History: 1500
  Leave Balances: 500

🔍 FAISS INDEXES:
  Employee Index: 500 vectors
  Attendance Index: 10000 vectors
  Leave Index: 1500 vectors
```

---

## ✅ Verification

### Check MongoDB:
```bash
# Open MongoDB shell
mongo

# Inside mongo shell:
use helix_hr_rag
show collections
db.employees.count()
exit
```

**Expected Output:**
```
employees
attendance_logs
leave_history
leave_balances

500
```

### Check FAISS Indexes:
```bash
# Windows:
dir faiss_indexes

# macOS/Linux:
ls -lh faiss_indexes/
```

**You should see:**
```
employees_index.faiss
employees_docs.pkl
attendance_index.faiss
attendance_docs.pkl
leave_index.faiss
leave_docs.pkl
```

---

## 🎮 First Query

Let's test the system!

```bash
python query_interface.py
```

**Try this query:**
```
💬 Your Query: Who is employee EMP1005?
```

**Expected Response:**
```
======================================================================
📝 ANSWER:
======================================================================
Employee EMP1005 is Calvin Nielsen, working in the Marketing 
department at the Bangalore location. He joined on April 20, 2024, 
and holds the position of Careers information officer with a salary 
band of D. His manager ID is EMP1497, and he is currently an active 
employee with an "Exceeds" performance rating. He holds a CISSP 
certification.

----------------------------------------------------------------------
📊 Confidence: 95% (high)
🔍 Search Method: structured
📚 Sources Found: 1
======================================================================
```

**🎉 Congratulations! Your RAG system is working!**

---

## 🐛 Troubleshooting

### Problem: "MongoDB connection failed"

**Cause:** MongoDB is not running

**Solution:**
```bash
# Windows:
net start MongoDB

# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongodb
sudo systemctl status mongodb
```

---

### Problem: "GROQ_API_KEY not set"

**Cause:** API key not configured

**Solution:**
```bash
# Set environment variable
export GROQ_API_KEY=your_key_here

# Or create .env file
echo "GROQ_API_KEY=your_key_here" > .env
```

---

### Problem: "ModuleNotFoundError: No module named 'pymongo'"

**Cause:** Virtual environment not activated or packages not installed

**Solution:**
```bash
# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall packages
pip install -r requirements.txt
```

---

### Problem: "FileNotFoundError: data/employee_master.csv"

**Cause:** Data files not in correct location

**Solution:**
```bash
# Check current directory
pwd  # macOS/Linux
cd   # Windows

# Verify data directory exists
ls data/  # macOS/Linux
dir data  # Windows

# Copy files to correct location
cp /path/to/files/*.csv data/
```

---

### Problem: "Out of memory" during ingestion

**Cause:** Large dataset or limited RAM

**Solution:**
1. **Reduce batch size** in `config.py`:
   ```python
   CHUNK_SIZE = 250  # Reduced from 500
   ```

2. **Process fewer records** in `ingest_data.py`:
   ```python
   # Sample attendance data
   attendance_sample = attendance[:5000]  # Reduced from 10000
   ```

---

### Problem: Slow query responses

**Cause:** CPU-only processing

**Solution:**
- **Normal**: 1-3 seconds is expected on CPU
- **Improve**: Reduce TOP_K_RESULTS in config.py
- **Alternative**: Use demo_standalone.py for faster testing

---

### Problem: "Invalid API key" error

**Cause:** Incorrect or expired Groq API key

**Solution:**
1. Verify key at https://console.groq.com
2. Check for extra spaces or quotes
3. Regenerate key if needed
4. Ensure key starts with `gsk_`

---

## 📚 Next Steps

### Immediate:
1. ✅ Try more queries in query_interface.py
2. ✅ Read README.md for full documentation
3. ✅ Run examples.py to see different usage patterns
4. ✅ Review BEGINNER_GUIDE.md for detailed explanations

### Short-term:
1. Customize config.py for your needs
2. Add more data sources
3. Experiment with different queries
4. Try demo_standalone.py for quick tests

### Long-term:
1. Build custom interfaces
2. Deploy to production
3. Add monitoring and logging
4. Scale with more data

---

## 🆘 Getting Help

### Resources:
- **README.md** - Full technical documentation
- **BEGINNER_GUIDE.md** - Step-by-step tutorial
- **PROJECT_SUMMARY.md** - System overview
- **Code comments** - Inline explanations in every file

### Common Commands:
```bash
# Check MongoDB status
mongo --version
pgrep mongod

# Check Python environment
python --version
pip list

# View logs
tail -f logs/*.log  # macOS/Linux
type logs\*.log     # Windows

# Restart MongoDB
# macOS: brew services restart mongodb-community
# Linux: sudo systemctl restart mongodb
# Windows: net stop MongoDB && net start MongoDB
```

---

## ✅ Installation Complete!

You should now have:
- ✅ MongoDB running
- ✅ Python environment configured
- ✅ All dependencies installed
- ✅ Data loaded into system
- ✅ FAISS indexes created
- ✅ Successful test query

**🚀 You're ready to start using the RAG system!**

---

**For detailed usage instructions, see:**
- README.md - Technical documentation
- BEGINNER_GUIDE.md - Beginner walkthrough
- examples.py - Code examples
