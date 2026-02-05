"""
Ingest Data for Helix RAG System
--------------------------------
This script loads data files (CSV/JSON/Excel/PDF),
stores them in MongoDB, generates embeddings, and
builds FAISS indexes for semantic search.
"""

import os
import logging
from rag_system import HybridRAGSystem  # Make sure this imports your RAG logic
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print("\n" + "="*60)
    print("🚀 HELIX RAG SYSTEM - DATA INGESTION")
    print("="*60, "\n")

    # --- File paths (automatic for convenience) ---
    BASE_DIR = os.path.join(os.path.dirname(__file__), "data")
    employee_csv = os.path.join(BASE_DIR, "employee_master.csv")
    attendance_json = os.path.join(BASE_DIR, "attendance_logs_detailed.json")
    leave_excel = os.path.join(BASE_DIR, "leave_intelligence.xlsx")
    policy_pdf = os.path.join(BASE_DIR, "Helix_Pro_Policy_v2.pdf")  # optional

    # Check files exist
    for file_path in [employee_csv, attendance_json, leave_excel]:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            print(f"❌ Missing file: {file_path}")
            return

    if not os.path.exists(policy_pdf):
        logger.warning(f"Optional PDF not found: {policy_pdf}")
        policy_pdf = None

    logger.info("✓ All input files verified")

    # --- Initialize RAG System ---
    rag = HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        gemini_api_key=os.getenv("GROQ_API_KEY")
    )

    # --- Load data and generate embeddings ---
    try:
        rag.load_and_index_data(
            employee_csv=employee_csv,
            attendance_json=attendance_json,
            leave_excel=leave_excel,
            policy_pdf=policy_pdf
        )
        logger.info("✓ Data loaded and indexed successfully")
    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
        print("\n❌ Data ingestion failed. Check file paths and formats.")
        rag.close()
        return

    # --- Save FAISS indexes ---
    try:
        rag.save_indexes()
        logger.info("✓ FAISS indexes saved successfully")
        print("\n✅ FAISS indexes saved successfully.")
    except Exception as e:
        logger.error(f"Error saving FAISS indexes: {e}")
        print("\n❌ Failed to save FAISS indexes.")
        rag.close()
        return

    # --- Close DB connection ---
    rag.close()
    print("\n✅ Data ingestion complete. You can now query the system using query_interface.py.\n")


if __name__ == "__main__":
    main()
