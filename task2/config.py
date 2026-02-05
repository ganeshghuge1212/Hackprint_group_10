"""
Configuration File for RAG System
----------------------------------
This file contains all configuration parameters for the RAG system.
Modify these settings based on your environment.
"""

import os

# ============================================
# MONGODB CONFIGURATION
# ============================================
MONGODB_URI = "mongodb://localhost:27017/"  # Change this to your MongoDB URI
DATABASE_NAME = "helix_hr_rag"
COLLECTIONS = {
    "employees": "employees",
    "attendance": "attendance_logs",
    "leave_history": "leave_history",
    "leave_balances": "leave_balances"
}

# ============================================
# EMBEDDING MODEL CONFIGURATION
# ============================================
# Using "all-MiniLM-L6-v2" - a lightweight, fast embedding model
# This is similar to "Mini LLM V6" mentioned in requirements
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # Dimension of the embedding vectors

# ============================================
# FAISS CONFIGURATION
# ============================================
FAISS_INDEX_PATH = "faiss_indexes"
FAISS_INDEX_FILES = {
    "employees": "employees_index.faiss",
    "attendance": "attendance_index.faiss",
    "leave": "leave_index.faiss"
}

# ============================================
# LLM CONFIGURATION (Groq API with Gemma)
# ============================================
# Using Groq API which provides fast inference for Gemma models
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Set in environment or .env file
LLM_MODEL = "gemma2-9b-it"  # Gemma 2 9B Instruct model via Groq

# ============================================
# RAG SYSTEM PARAMETERS
# ============================================
TOP_K_RESULTS = 5  # Number of similar documents to retrieve
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score (0-1)
MAX_CONTEXT_LENGTH = 4000  # Maximum context to send to LLM

# ============================================
# DATA PROCESSING PARAMETERS
# ============================================
CHUNK_SIZE = 500  # Characters per text chunk for long documents
CHUNK_OVERLAP = 50  # Overlap between chunks

# ============================================
# PATHS
# ============================================
DATA_DIR = "data"
PROCESSED_DATA_DIR = "processed_data"
LOGS_DIR = "logs"
