"""
Interactive Query Interface for Helix RAG System
------------------------------------------------
Allows users to ask questions in real-time.
"""

import os
from rag_system import HybridRAGSystem
import config

def print_header():
    print("\n" + "="*60)
    print("💬 HELIX RAG SYSTEM - INTERACTIVE MODE")
    print("="*60, "\n")
    print("Type 'exit' to quit at any time.\n")

def main():
    # Initialize RAG system
    rag = HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        gemini_api_key=os.getenv("GROQ_API_KEY")
    )

    # Load FAISS indexes
    print("📂 Loading FAISS indexes...")
    rag.load_indexes()
    print("✅ Indexes loaded.\n")

    print_header()

    while True:
        query_text = input("❓ Enter your question: ").strip()
        if query_text.lower() in ["exit", "quit"]:
            print("\n👋 Exiting interactive mode...")
            break

        # Decide whether to use structured search first
        use_structured = True

        # Get response from RAG
        response = rag.query(query_text, use_structured=use_structured)

        # Display response
        print("\n📖 Answer:")
        print(response["answer"])
        print(f"\n🔹 Confidence: {response['confidence']:.2f}")
        print(f"🔹 Sources used: {response.get('source_count', 0)}")
        print(f"🔹 Search Method: {response.get('search_method', 'semantic')}")
        print("-"*60, "\n")

    # Close RAG system
    rag.close()
    print("✅ Interactive session ended.\n")

if __name__ == "__main__":
    main()
