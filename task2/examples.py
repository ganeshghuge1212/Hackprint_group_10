"""
Example Usage Script
--------------------
This script demonstrates how to use the RAG system programmatically.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from rag_system import HybridRAGSystem
import config

def example_basic_query():
    """
    Example 1: Basic query usage
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Query")
    print("="*70)
    
    # Read API key from your saved file
    with open('/mnt/user-data/uploads/1770275466020_groq_api_key.txt', 'r') as f:
        api_key = f.readline().split(': ')[1].strip()
    
    # Initialize RAG system
    rag = HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        groq_api_key=api_key
    )
    
    # Load pre-built indexes
    if os.path.exists(config.FAISS_INDEX_PATH):
        rag.load_indexes()
    
    # Query the system
    query = "What is the leave policy for Singapore employees?"
    print(f"\nQuery: {query}\n")
    
    response = rag.query(query)
    
    print("Answer:")
    print(response['answer'])
    print(f"\nConfidence: {response['confidence']:.2%}")
    print(f"Sources: {response['source_count']}")
    
    rag.close()


def example_multiple_queries():
    """
    Example 2: Multiple queries in sequence
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Multiple Queries")
    print("="*70)
    
    # Read API key
    with open('/mnt/user-data/uploads/1770275466020_groq_api_key.txt', 'r') as f:
        api_key = f.readline().split(': ')[1].strip()
    
    # Initialize
    rag = HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        groq_api_key=api_key
    )
    
    if os.path.exists(config.FAISS_INDEX_PATH):
        rag.load_indexes()
    
    # Multiple queries
    queries = [
        "How many employees are in the Engineering department?",
        "What happens if someone misses check-out 5 times?",
        "What are the tenure-based benefits?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i} ---")
        print(f"Q: {query}")
        
        response = rag.query(query)
        print(f"A: {response['answer'][:200]}...")  # First 200 chars
        print(f"Confidence: {response['confidence']:.2%}")
    
    rag.close()


def example_structured_query():
    """
    Example 3: Direct structured query to MongoDB
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Structured Database Query")
    print("="*70)
    
    with open('/mnt/user-data/uploads/1770275466020_groq_api_key.txt', 'r') as f:
        api_key = f.readline().split(': ')[1].strip()
    
    rag = HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        groq_api_key=api_key
    )
    
    # Direct MongoDB query
    print("\nQuerying MongoDB for employees in Singapore...")
    results = rag.query_structured(
        collection=config.COLLECTIONS['employees'],
        query={'location': 'Singapore'}
    )
    
    print(f"\nFound {len(results)} employees in Singapore:")
    for emp in results[:5]:  # Show first 5
        print(f"  - {emp.get('name')} ({emp.get('emp_id')}) - {emp.get('dept')}")
    
    rag.close()


def example_semantic_search():
    """
    Example 4: Pure semantic search
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Semantic Search")
    print("="*70)
    
    with open('/mnt/user-data/uploads/1770275466020_groq_api_key.txt', 'r') as f:
        api_key = f.readline().split(': ')[1].strip()
    
    rag = HybridRAGSystem(
        mongodb_uri=config.MONGODB_URI,
        database_name=config.DATABASE_NAME,
        groq_api_key=api_key
    )
    
    if os.path.exists(config.FAISS_INDEX_PATH):
        rag.load_indexes()
    
    # Semantic search
    query = "software engineers with certifications"
    print(f"\nSemantic search for: {query}")
    
    results = rag.query_semantic(query, index_name='employees', k=5)
    
    print(f"\nTop {len(results)} matches:")
    for doc, similarity in results:
        name = doc.get('name', 'Unknown')
        dept = doc.get('dept', 'Unknown')
        certs = doc.get('certifications', 'None')
        print(f"  - {name} ({dept}) - Certs: {certs} - Similarity: {similarity:.2%}")
    
    rag.close()


def example_custom_prompt():
    """
    Example 5: Using the LLM interface directly
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Custom LLM Prompt")
    print("="*70)
    
    with open('/mnt/user-data/uploads/1770275466020_groq_api_key.txt', 'r') as f:
        api_key = f.readline().split(': ')[1].strip()
    
    from llm_interface import GroqLLMInterface
    
    llm = GroqLLMInterface(api_key, config.LLM_MODEL)
    
    prompt = """
    You are an HR policy expert. Explain the following in simple terms:
    
    "Employees with 5+ years of tenure get an additional 5 days of annual leave."
    
    Provide a clear, friendly explanation.
    """
    
    response = llm.generate_response(prompt, max_tokens=300)
    
    print("\nLLM Response:")
    print(response)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  RAG SYSTEM - USAGE EXAMPLES")
    print("="*70)
    
    print("\nAvailable examples:")
    print("1. Basic Query")
    print("2. Multiple Queries")
    print("3. Structured Database Query")
    print("4. Semantic Search")
    print("5. Custom LLM Prompt")
    print("6. Run All Examples")
    
    choice = input("\nSelect example (1-6): ").strip()
    
    try:
        if choice == "1":
            example_basic_query()
        elif choice == "2":
            example_multiple_queries()
        elif choice == "3":
            example_structured_query()
        elif choice == "4":
            example_semantic_search()
        elif choice == "5":
            example_custom_prompt()
        elif choice == "6":
            example_basic_query()
            example_multiple_queries()
            example_structured_query()
            example_semantic_search()
            example_custom_prompt()
        else:
            print("Invalid choice")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. MongoDB is running")
        print("  2. Data has been ingested (run ingest_data.py)")
        print("  3. API key is valid")
