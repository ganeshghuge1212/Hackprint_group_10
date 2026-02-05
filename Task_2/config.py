"""
Configuration for Helix RAG System
----------------------------------
This file contains all configurable parameters including:
- LLM model and API keys
- Embedding model and dimensions
- MongoDB connection and collections
- FAISS index paths
- RAG system parameters
- Data processing parameters
- Project directory paths
"""

import os

# ================= LLM / AI MODEL CONFIG =================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Your Gemini API key
LLM_MODEL = "gemini-1.5-flash"                    # Language model

# ================= EMBEDDING CONFIG =================
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # Dimension of embedding vectors

# ================= MONGODB CONFIG =================
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "helix_hr_rag"
COLLECTIONS = {
    "employees": "employees",
    "attendance": "attendance_logs",
    "leave_history": "leave_history",
    "leave_balances": "leave_balances"
}

# ================= FAISS CONFIG =================
FAISS_INDEX_PATH = os.path.join(os.getcwd(), "faiss_indexes")  # Folder to save FAISS indexes

# ================= RAG SYSTEM PARAMETERS =================
TOP_K_RESULTS = 5
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity to consider a match
MAX_CONTEXT_LENGTH = 4000   # Maximum tokens/characters to retrieve as context

# ================= DATA PROCESSING =================
CHUNK_SIZE = 500       # Split large documents into chunks of this size
CHUNK_OVERLAP = 50     # Number of overlapping characters between chunks

# ================= PROJECT DIRECTORY PATHS =================
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")                   # Raw input data
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "processed_data")  # Processed/cleaned data
LOGS_DIR = os.path.join(BASE_DIR, "logs")                   # Log files

# Safe directory creation: only create if it doesn't exist as folder
for folder in [DATA_DIR, PROCESSED_DATA_DIR, LOGS_DIR, FAISS_INDEX_PATH]:
    if os.path.exists(folder):
        if not os.path.isdir(folder):
            # If a file exists with the same name, remove it first
            os.remove(folder)
            os.makedirs(folder, exist_ok=True)
    else:
        os.makedirs(folder, exist_ok=True)

# ================= HELPER FUNCTION =================
def print_config():
    """
    Prints key configuration values for verification
    """
    print("=== Helix RAG System Configuration ===")
    print(f"LLM Model: {LLM_MODEL}")
    print(f"Embedding Model: {EMBEDDING_MODEL} ({EMBEDDING_DIMENSION} dims)")
    print(f"MongoDB URI: {MONGODB_URI}")
    print(f"Database Name: {DATABASE_NAME}")
    print(f"FAISS Index Path: {FAISS_INDEX_PATH}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Processed Data Directory: {PROCESSED_DATA_DIR}")
    print(f"Logs Directory: {LOGS_DIR}")
    print("======================================")
