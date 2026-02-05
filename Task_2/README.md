# Helix HR RAG System

A complete Retrieval-Augmented Generation (RAG) system for HR data using MongoDB, FAISS, Mini LLM embeddings, and Gemma LLM.

## 🎯 Project Overview

This RAG system combines:
- **MongoDB** for structured data storage
- **FAISS** for fast similarity search
- **Mini LLM (all-MiniLM-L6-v2)** for generating embeddings
- **Gemma 2 9B** (via Groq API) for natural language responses

## 📋 Features

- ✅ Hybrid search (structured + semantic)
- ✅ Multi-index vector storage
- ✅ Intelligent query routing
- ✅ Source attribution and confidence scoring
- ✅ Interactive query interface
- ✅ Policy-aware responses

## 🛠️ System Requirements

### Software Requirements
- Python 3.8 or higher
- MongoDB 4.4 or higher
- 4GB+ RAM (8GB recommended)
- Internet connection (for downloading models and API calls)

### Required APIs
- **Groq API Key** (free tier available at https://console.groq.com)

## 📦 Installation

### Step 1: Clone/Download the Project

```bash
# Create project directory
mkdir helix_rag_system
cd helix_rag_system

# Copy all Python files to this directory
```

### Step 2: Install MongoDB

**Ubuntu/Debian:**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Windows:**
- Download from https://www.mongodb.com/try/download/community
- Install and start MongoDB service

**Verify Installation:**
```bash
mongo --version
# Should show: MongoDB shell version v4.4.x or higher
```

### Step 3: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

**Note:** First installation may take 5-10 minutes as it downloads:
- Sentence transformers models (~400MB)
- PyTorch (~700MB)
- Other dependencies

### Step 4: Setup Groq API Key

1. Get your free API key from https://console.groq.com
2. Set it as an environment variable:

**Linux/Mac:**
```bash
export GROQ_API_KEY='your_api_key_here'
```

**Windows:**
```cmd
set GROQ_API_KEY=your_api_key_here
```

**Or create a .env file:**
```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### Step 5: Prepare Data Files

Create a `data/` directory and place your files:

```bash
mkdir data
# Copy your data files to the data/ directory:
# - employee_master.csv
# - attendance_logs_detailed.json
# - leave_intelligence.xlsx
# - Helix_Pro_Policy_v2.pdf (optional)
```

## 🚀 Usage

### Initial Setup (One-Time)

Run the data ingestion script to load data and create indexes:

```bash
python ingest_data.py
```

This will:
1. ✅ Load all data files
2. ✅ Clean and normalize data
3. ✅ Store in MongoDB
4. ✅ Generate embeddings using Mini LLM
5. ✅ Create FAISS indexes
6. ✅ Save indexes to disk

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

[2/4] Loading Attendance Data...
✓ Loaded JSON file: data/attendance_logs_detailed.json
  Top-level keys: 500

... (more output) ...

✅ DATA INGESTION COMPLETE!
```

**Time Estimate:** 2-5 minutes depending on your hardware

### Running Queries

Start the interactive query interface:

```bash
python query_interface.py
```

**Example Session:**
```
============================================================
HELIX HR RAG SYSTEM - QUERY INTERFACE
============================================================

🚀 Initializing RAG System...
✅ System ready!

============================================================
EXAMPLE QUERIES
============================================================

1. Who is employee EMP1005?
2. List employees in the Engineering department
3. What is the leave policy for Singapore employees?
4. Show me attendance records with missing check-outs
5. How many days of annual leave do employees get after 5 years?

💬 Your Query: Who is employee EMP1005?

======================================================================
📝 ANSWER:
======================================================================
Employee EMP1005 is Calvin Nielsen, working in the Marketing department
at the Bangalore location. He joined on April 20, 2024, and holds the
position of Careers information officer with a salary band of D...

----------------------------------------------------------------------
📊 Confidence: 95% (high)
🔍 Search Method: structured
📚 Sources Found: 1
======================================================================
```

## 📚 Query Examples

### Employee Queries
```python
"Who is employee EMP1001?"
"Show me details for Patrick Sanchez"
"List all employees in the Engineering department"
"Find employees located in Singapore"
"How many employees work in Tokyo?"
```

### Attendance Queries
```python
"Show attendance for EMP1005 in November 2025"
"Find employees with missing check-outs"
"What are the attendance violations this month?"
"Show me who hasn't checked out today"
```

### Leave Queries
```python
"What is the annual leave policy?"
"How much leave does EMP1001 have available?"
"What are the sick leave requirements for Singapore employees?"
"Explain tenure-based leave benefits"
"Can I carry forward unused annual leave?"
```

### Policy Queries
```python
"What happens if I miss check-out 5 times?"
"What is the disciplinary policy for attendance?"
"Are there any regional policy differences?"
"What benefits do employees get after 5 years?"
```

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER QUERY                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   HYBRID RAG SYSTEM                         │
│  ┌──────────────────┐         ┌─────────────────────────┐  │
│  │ Structured Query │         │   Semantic Search       │  │
│  │    (MongoDB)     │         │      (FAISS)            │  │
│  └────────┬─────────┘         └──────────┬──────────────┘  │
│           │                               │                 │
│           └───────────┬───────────────────┘                 │
│                       ▼                                     │
│           ┌────────────────────────┐                        │
│           │  Retrieved Documents   │                        │
│           └────────────┬───────────┘                        │
│                        ▼                                    │
│           ┌────────────────────────┐                        │
│           │  Prompt Builder        │                        │
│           └────────────┬───────────┘                        │
│                        ▼                                    │
│           ┌────────────────────────┐                        │
│           │  Gemma 2 9B LLM        │                        │
│           │    (via Groq)          │                        │
│           └────────────┬───────────┘                        │
│                        ▼                                    │
└────────────────────────┴────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            FORMATTED RESPONSE + SOURCES                     │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
helix_rag_system/
├── config.py                  # Configuration settings
├── database_handler.py        # MongoDB operations
├── data_loader.py             # Data loading and preprocessing
├── embedding_generator.py     # Embedding generation (Mini LLM)
├── faiss_vector_store.py      # FAISS index management
├── llm_interface.py           # Groq/Gemma LLM interface
├── rag_system.py              # Main RAG orchestrator
├── ingest_data.py             # Data ingestion script
├── query_interface.py         # Interactive query interface
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── data/                      # Data directory
│   ├── employee_master.csv
│   ├── attendance_logs_detailed.json
│   ├── leave_intelligence.xlsx
│   └── Helix_Pro_Policy_v2.pdf
└── faiss_indexes/             # Saved FAISS indexes
    ├── employees_index.faiss
    ├── employees_docs.pkl
    ├── attendance_index.faiss
    ├── attendance_docs.pkl
    ├── leave_index.faiss
    └── leave_docs.pkl
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# MongoDB settings
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "helix_hr_rag"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# LLM settings
LLM_MODEL = "gemma2-9b-it"

# RAG parameters
TOP_K_RESULTS = 5              # Number of documents to retrieve
SIMILARITY_THRESHOLD = 0.3     # Minimum similarity score
```

## 🧪 Testing the System

### Quick Test

```python
from rag_system import HybridRAGSystem
import config

# Initialize
rag = HybridRAGSystem(
    mongodb_uri=config.MONGODB_URI,
    database_name=config.DATABASE_NAME,
    groq_api_key="your_api_key"
)

# Load indexes
rag.load_indexes()

# Test query
response = rag.query("What is the leave policy?")
print(response['answer'])

# Close
rag.close()
```

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Error: Failed to connect to MongoDB
```
**Solution:**
- Ensure MongoDB is running: `sudo systemctl status mongodb`
- Check connection string in `config.py`
- Try: `mongo` command to test connection

### Groq API Error
```
Error: Invalid API key
```
**Solution:**
- Verify API key at https://console.groq.com
- Check environment variable: `echo $GROQ_API_KEY`
- Ensure no extra spaces in the key

### Out of Memory Error
```
RuntimeError: CUDA out of memory
```
**Solution:**
- System automatically uses CPU if no GPU
- Reduce `CHUNK_SIZE` in `config.py`
- Process fewer documents at once

### No Results Found
```
I couldn't find relevant information...
```
**Solution:**
- Try more specific queries
- Lower `SIMILARITY_THRESHOLD` in `config.py`
- Check if data was properly ingested

## 📊 Performance Notes

- **Initial Setup:** 2-5 minutes
- **Query Response Time:** 1-3 seconds
- **Memory Usage:** ~2GB RAM
- **Index Size:** ~100-500MB depending on data

## 🔒 Security Notes

- Store API keys securely (use environment variables)
- Don't commit `.env` file to version control
- MongoDB should not be exposed to the internet
- Use authentication for production deployments

## 🤝 Contributing

To extend the system:

1. **Add new data sources:** Modify `data_loader.py`
2. **Change embedding model:** Update `config.py`
3. **Customize prompts:** Edit `llm_interface.py`
4. **Add new indexes:** Extend `rag_system.py`

## 📝 License

This project is for educational purposes. Ensure compliance with:
- Anthropic's usage policies (for Claude)
- Groq's terms of service
- MongoDB license
- FAISS license (MIT)

## 🆘 Support

For issues:
1. Check logs in console output
2. Review this README
3. Check configuration in `config.py`
4. Ensure all dependencies are installed

## 🎓 Learning Resources

- **RAG Systems:** https://python.langchain.com/docs/use_cases/question_answering/
- **FAISS:** https://github.com/facebookresearch/faiss/wiki
- **Sentence Transformers:** https://www.sbert.net/
- **MongoDB:** https://docs.mongodb.com/
- **Groq API:** https://console.groq.com/docs

---

**Happy Querying! 🚀**
