"""
Examples for Helix RAG System
-----------------------------
Demonstrates structured and semantic queries on the RAG system.
"""

import os
from rag_system import HybridRAGSystem
import config

def main():
    print("\n" + "="*60)
    print("💡 HELIX RAG SYSTEM - EXAMPLES")
    print("="*60, "\n")

    # Initialize RAG System
    rag = HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        gemini_api_key=os.getenv("GROQ_API_KEY")
    )

    # Load FAISS indexes from disk
    print("📂 Loading FAISS indexes...")
    rag.load_indexes()
    print("✅ Indexes loaded.\n")

    # Example 1: Structured Query by Employee ID
    query1 = "Employee emp1001"
    print(f"📝 Example 1 - Structured Query: {query1}")
    result1 = rag.query(query1)
    print("Answer:", result1["answer"])
    print("Confidence:", result1["confidence"])
    print("Sources:", result1["source_count"])
    print("-"*50, "\n")

    # Example 2: Structured Query by Employee Name
    query2 = "Tell me about employee Alice"
    print(f"📝 Example 2 - Structured Query by Name: {query2}")
    result2 = rag.query(query2)
    print("Answer:", result2["answer"])
    print("Confidence:", result2["confidence"])
    print("Sources:", result2["source_count"])
    print("-"*50, "\n")

    # Example 3: Semantic Query
    query3 = "What is the leave policy for sick leave?"
    print(f"📝 Example 3 - Semantic Query: {query3}")
    result3 = rag.query(query3, use_structured=False)
    print("Answer:", result3["answer"])
    print("Confidence:", result3["confidence"])
    print("Sources:", result3["source_count"])
    print("-"*50, "\n")

    # Example 4: Semantic Query about Attendance
    query4 = "Who was absent last Friday?"
    print(f"📝 Example 4 - Semantic Query: {query4}")
    result4 = rag.query(query4, use_structured=False)
    print("Answer:", result4["answer"])
    print("Confidence:", result4["confidence"])
    print("Sources:", result4["source_count"])
    print("-"*50, "\n")

    # Close RAG system
    rag.close()
    print("✅ Examples completed.\n")

if __name__ == "__main__":
    main()
