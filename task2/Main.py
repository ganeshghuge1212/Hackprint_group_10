"""
Main Entry Point for Helix RAG System
--------------------------------------
This is a unified entry point that guides you through the system.
"""

import os
import sys

def print_header():
    print("\n" + "="*70)
    print("  HELIX HR RAG SYSTEM")
    print("="*70)

def main_menu():
    print_header()
    print("\nWhat would you like to do?\n")
    print("1. 📥 Load Data (First-time setup)")
    print("2. 💬 Ask Questions (Interactive mode)")
    print("3. 📚 See Examples (Learn the system)")
    print("4. 🚀 Quick Demo (No MongoDB required)")
    print("5. ⚙️  Check System Status")
    print("6. 📖 View Documentation")
    print("7. ❌ Exit")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    return choice

def check_status():
    """Check if system is ready."""
    print("\n" + "="*70)
    print("  SYSTEM STATUS CHECK")
    print("="*70)
    
    # Check Python
    print("\n✓ Python:", sys.version.split()[0])
    
    # Check packages
    print("\nChecking installed packages...")
    required = ['pymongo', 'faiss', 'sentence_transformers', 'groq', 'pandas']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_'))
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg} - NOT INSTALLED")
            missing.append(pkg)
    
    # Check MongoDB
    print("\nChecking MongoDB...")
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("  ✓ MongoDB is running")
        client.close()
    except:
        print("  ✗ MongoDB not running or not installed")
    
    # Check API key
    print("\nChecking Groq API Key...")
    if os.getenv('GROQ_API_KEY'):
        print("  ✓ GROQ_API_KEY is set")
    else:
        print("  ✗ GROQ_API_KEY not set")
    
    # Check data
    print("\nChecking data files...")
    data_dir = "data"
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        if files:
            print(f"  ✓ Found {len(files)} files in data/")
        else:
            print("  ✗ data/ folder is empty")
    else:
        print("  ✗ data/ folder not found")
    
    if missing:
        print("\n⚠️  Missing packages. Install with:")
        print("  pip install -r requirements.txt")
    else:
        print("\n✅ All packages installed!")
    
    input("\nPress Enter to continue...")

def view_docs():
    """Show available documentation."""
    print("\n" + "="*70)
    print("  DOCUMENTATION")
    print("="*70)
    
    docs = {
        "START_HERE.md": "Overview and getting started",
        "INSTALLATION.md": "Step-by-step installation guide",
        "BEGINNER_GUIDE.md": "Complete beginner tutorial",
        "README.md": "Technical documentation",
        "PROJECT_SUMMARY.md": "Architecture and design"
    }
    
    print("\nAvailable documentation:\n")
    for doc, desc in docs.items():
        exists = "✓" if os.path.exists(doc) else "✗"
        print(f"  {exists} {doc}")
        print(f"     {desc}")
    
    print("\n💡 Tip: Open these .md files in any text editor!")
    input("\nPress Enter to continue...")

def main():
    """Main program loop."""
    while True:
        choice = main_menu()
        
        if choice == "1":
            print("\n🚀 Starting data ingestion...")
            print("This will load your data into the system.\n")
            os.system("python ingest_data.py")
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            print("\n💬 Starting interactive mode...")
            os.system("python query_interface.py")
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            print("\n📚 Running examples...")
            os.system("python examples.py")
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print("\n🚀 Starting quick demo...")
            os.system("python demo_standalone.py")
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            check_status()
        
        elif choice == "6":
            view_docs()
        
        elif choice == "7":
            print("\n👋 Goodbye!\n")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter 1-7.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)