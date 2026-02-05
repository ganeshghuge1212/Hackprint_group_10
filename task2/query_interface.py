"""
Interactive Query Interface
----------------------------
This script provides an interactive interface to query the RAG system.
"""

import logging
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from rag_system import HybridRAGSystem
from llm_interface import ResponseFormatter
import config

# Setup logging
logging.basicConfig(
    level=logging.WARNING,  # Set to WARNING to reduce noise during interaction
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_response(response: dict) -> None:
    """
    Pretty print the response.
    
    Args:
        response: Response dictionary from RAG system
    """
    print("\n" + "=" * 70)
    print("📝 ANSWER:")
    print("=" * 70)
    print(response['answer'])
    
    print("\n" + "-" * 70)
    print(f"📊 Confidence: {response['confidence']:.2%} ({response['metadata']['confidence_level']})")
    print(f"🔍 Search Method: {response['search_method']}")
    print(f"📚 Sources Found: {response['source_count']}")
    
    if response['sources']:
        print("\n" + "-" * 70)
        print("📖 SOURCE REFERENCES:")
        print("-" * 70)
        refs = ResponseFormatter.format_source_references(response['sources'][:3])  # Show top 3
        print(refs)
    
    print("=" * 70)


def run_example_queries(rag: HybridRAGSystem) -> None:
    """
    Run some example queries to demonstrate the system.
    
    Args:
        rag: RAG system instance
    """
    example_queries = [
        "Who is employee EMP1005?",
        "List employees in the Engineering department",
        "What is the leave policy for Singapore employees?",
        "Show me attendance records with missing check-outs",
        "How many days of annual leave do employees get after 5 years?"
    ]
    
    print("\n" + "=" * 70)
    print(" EXAMPLE QUERIES")
    print("=" * 70)
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n{i}. {query}")
    
    print("\n" + "=" * 70)
    
    while True:
        choice = input("\nEnter query number (1-5) or 'skip' to continue: ").strip()
        
        if choice.lower() == 'skip':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(example_queries):
                query = example_queries[idx]
                print(f"\n🔍 Query: {query}")
                response = rag.query(query)
                print_response(response)
                break
            else:
                print("Invalid choice. Please enter 1-5.")
        except ValueError:
            print("Invalid input. Please enter a number or 'skip'.")


def interactive_mode(rag: HybridRAGSystem) -> None:
    """
    Run interactive query mode.
    
    Args:
        rag: RAG system instance
    """
    print("\n" + "=" * 70)
    print(" INTERACTIVE MODE")
    print("=" * 70)
    print("\nEnter your queries below. Type 'exit' or 'quit' to stop.")
    print("Type 'help' for tips on writing effective queries.")
    
    while True:
        try:
            print("\n" + "-" * 70)
            query = input("💬 Your Query: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == 'help':
                print_help()
                continue
            
            # Process query
            response = rag.query(query)
            print_response(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            logger.error(f"Error processing query: {e}", exc_info=True)


def print_help() -> None:
    """Print help information."""
    print("\n" + "=" * 70)
    print(" QUERY TIPS")
    print("=" * 70)
    print("""
📌 EFFECTIVE QUERIES:

1. EMPLOYEE QUERIES:
   - "Who is employee EMP1001?"
   - "Show me details for John Smith"
   - "List all employees in Engineering department"
   - "Find employees in Singapore location"

2. ATTENDANCE QUERIES:
   - "Show attendance for EMP1005 in November"
   - "Find all employees with missing check-outs"
   - "What are the attendance violations this month?"

3. LEAVE QUERIES:
   - "What is the annual leave policy?"
   - "How much leave does employee EMP1001 have?"
   - "What are the leave requirements for Singapore?"
   - "Explain the tenure-based leave benefits"

4. POLICY QUERIES:
   - "What is the sick leave policy?"
   - "What happens if I miss check-out more than 5 times?"
   - "What are the regional policy variations?"

💡 TIPS:
   - Be specific: mention employee IDs, dates, or departments
   - Ask one question at a time
   - Use natural language - the system understands context
    """)
    print("=" * 70)


def main():
    """
    Main function for interactive query interface.
    """
    print("\n" + "=" * 70)
    print(" HELIX HR RAG SYSTEM - QUERY INTERFACE")
    print("=" * 70)
    
    try:
        # Check if Groq API key is set
        if not config.GROQ_API_KEY:
            print("\n❌ ERROR: GROQ_API_KEY not set!")
            print("Please set it as an environment variable or in a .env file")
            return
        
        # Initialize RAG system
        print("\n🚀 Initializing RAG System...")
        rag = HybridRAGSystem(
            mongodb_uri=config.MONGODB_URI,
            database_name=config.DATABASE_NAME,
            groq_api_key=config.GROQ_API_KEY
        )
        
        # Check if data is loaded
        from database_handler import MongoDBHandler
        db_check = MongoDBHandler(config.MONGODB_URI, config.DATABASE_NAME)
        emp_count = db_check.count_documents(config.COLLECTIONS['employees'])
        db_check.close()
        
        if emp_count == 0:
            print("\n⚠️  WARNING: No data found in database!")
            print("Please run 'python ingest_data.py' first to load data.")
            return
        
        # Try to load indexes
        if os.path.exists(config.FAISS_INDEX_PATH):
            print("📂 Loading FAISS indexes...")
            rag.load_indexes()
        else:
            print("\n⚠️  WARNING: FAISS indexes not found!")
            print("Please run 'python ingest_data.py' first to create indexes.")
            return
        
        print("✅ System ready!")
        
        # Run example queries first
        run_example_queries(rag)
        
        # Start interactive mode
        interactive_mode(rag)
        
        # Close connection
        rag.close()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("  1. MongoDB is running")
        print("  2. Data has been ingested (run ingest_data.py)")
        print("  3. Groq API key is valid")
        sys.exit(1)


if __name__ == "__main__":
    main()
