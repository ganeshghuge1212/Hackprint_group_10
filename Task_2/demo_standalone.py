"""
Quick Demo for Helix RAG System
-------------------------------
Runs a standalone demo using FAISS indexes and Gemini LLM
without needing MongoDB.
"""

import os
from rag_system import HybridRAGSystem
import config

def run_demo():
    print("\n" + "="*70)
    print("🚀 HELIX RAG SYSTEM - QUICK DEMO")
    print("="*70)

    # Initialize RAG system (MongoDB not required for demo)
    rag = HybridRAGSystem(
        mongodb_uri="",  # Not used in demo
        database_name="",
        gemini_api_key=os.getenv("GROQ_API_KEY")
    )

    # Load FAISS indexes
    if os.path.exists(config.FAISS_INDEX_PATH):
        print("📂 Loading FAISS indexes...")
        rag.load_indexes()
        print("✅ FAISS indexes loaded\n")
    else:
        print("⚠️ FAISS indexes not found. Please run ingest_data.py first!\n")
        return

    print("💬 You can now ask questions! Type 'exit' to quit.\n")

    while True:
        query = input("Your Question: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("\n👋 Exiting demo.")
            break
        if not query:
            continue

        # Run semantic query only (no structured query)
        response = rag.query(query, use_structured=False)

        print("\n💡 Answer:\n", response.get("answer", "No answer found."))
        print("📊 Confidence:", f"{response.get('confidence', 0.0):.2f}")
        print("🔍 Search Method:", response.get("search_method", "N/A"))
        print("Sources Retrieved:", len(response.get("sources", [])))
        print("-"*60)

    rag.close()

if __name__ == "__main__":
    run_demo()
