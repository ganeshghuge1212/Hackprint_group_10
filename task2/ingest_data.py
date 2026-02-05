"""
Data Ingestion Script
---------------------
Loads data into MongoDB and builds FAISS index.
Run this ONCE.
"""

import sys
import os
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).parent))

from rag_system import HybridRAGSystem
import config

logging.basicConfig(level=logging.INFO)

def read_groq_api_key():
    key_path = "data/groq_api_key.txt"
    if not os.path.exists(key_path):
        raise FileNotFoundError("❌ groq_api_key.txt not found in data/")
    with open(key_path, "r") as f:
        return f.read().strip()

def main():
    print("\n" + "="*60)
    print(" HELIX RAG SYSTEM - DATA INGESTION ")
    print("="*60)

    # ✅ YOUR DATA PATHS
    EMPLOYEE_CSV = "data/employee_master.csv"
    ATTENDANCE_JSON = "data/attendance_logs_detailed.json"
    LEAVE_EXCEL = "data/leave_intelligence.xlsx"
    POLICY_PDF = "data/Helix_Pro_Policy_v2.pdf"

    # Check files
    files = [EMPLOYEE_CSV, ATTENDANCE_JSON, LEAVE_EXCEL]
    missing = [f for f in files if not os.path.exists(f)]

    if missing:
        print("\n❌ Missing files:")
        for m in missing:
            print(" -", m)
        return

    try:
        groq_api_key = read_groq_api_key()

        print("\n🚀 Initializing RAG system...")
        rag = HybridRAGSystem(
            mongodb_uri=config.MONGODB_URI,
            database_name=config.DATABASE_NAME,
            groq_api_key=groq_api_key
        )

        print("\n📥 Loading & indexing data (wait patiently)...\n")

        rag.load_and_index_data(
            employee_csv=EMPLOYEE_CSV,
            attendance_json=ATTENDANCE_JSON,
            leave_excel=LEAVE_EXCEL,
            policy_pdf=POLICY_PDF if os.path.exists(POLICY_PDF) else None
        )

        print("\n💾 Saving FAISS index...")
        rag.save_indexes()

        print("\n✅ DATA INGESTION COMPLETED SUCCESSFULLY")
        print("👉 Next run: python query_interface.py\n")

        rag.close()

    except Exception as e:
        print("\n❌ ERROR:")
        print(e)
        print("\nChecklist:")
        print("✔ MongoDB running (mongod)")
        print("✔ Data files inside data/")
        print("✔ groq_api_key.txt present")
        sys.exit(1)

if __name__ == "__main__":
    main()
