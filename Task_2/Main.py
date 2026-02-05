"""
Main Entry Point for Helix RAG System (Gemini Version)
-----------------------------------------------------
Unified launcher for Gemini 1.5 Flash based RAG system
"""

import os
import sys

def print_header():
    print("\n" + "=" * 70)
    print("  HELIX HR RAG SYSTEM  |  GEMINI 1.5 FLASH")
    print("=" * 70)

def main_menu():
    print_header()
    print("\nWhat would you like to do?\n")
    print("1. 📥 Load Data (Create FAISS Index)")
    print("2. 💬 Ask Questions (RAG Query)")
    print("3. 🚀 Quick Demo (Standalone RAG)")
    print("4. ⚙️  Check System Status")
    print("5. 📖 View Documentation")
    print("6. ❌ Exit")

    return input("\nEnter your choice (1-6): ").strip()

def check_status():
    print("\n" + "=" * 70)
    print("  SYSTEM STATUS CHECK")
    print("=" * 70)

    # Python
    print("\n✓ Python Version:", sys.version.split()[0])

    # Required packages
    print("\nChecking installed packages...")
    required = [
        "google.generativeai",
        "faiss",
        "sentence_transformers",
        "streamlit",
        "numpy"
    ]

    missing = []
    for pkg in required:
        try:
            __import__(pkg.split(".")[0])
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg} - NOT INSTALLED")
            missing.append(pkg)

    # Gemini API Key
    print("\nChecking Gemini API Key...")
    if os.getenv("GOOGLE_API_KEY"):
        print("  ✓ GOOGLE_API_KEY is set")
    else:
        print("  ✗ GOOGLE_API_KEY not set")

    # Data folder
    print("\nChecking data folder...")
    if os.path.exists("data"):
        files = os.listdir("data")
        if files:
            print(f"  ✓ Found {len(files)} files in data/")
        else:
            print("  ⚠️ data/ folder is empty")
    else:
        print("  ⚠️ data/ folder not found")

    if missing:
        print("\n⚠️ Missing packages detected")
        print("Install using:")
        print("pip install streamlit google-generativeai faiss-cpu sentence-transformers numpy")
    else:
        print("\n✅ System is READY")

    input("\nPress Enter to continue...")

def view_docs():
    print("\n" + "=" * 70)
    print("  DOCUMENTATION")
    print("=" * 70)

    docs = [
        "README.md",
        "INSTALLATION.md",
        "PROJECT_SUMMARY.md"
    ]

    for doc in docs:
        status = "✓" if os.path.exists(doc) else "✗"
        print(f"  {status} {doc}")

    input("\nPress Enter to continue...")

def main():
    while True:
        choice = main_menu()

        if choice == "1":
            print("\n📥 Loading data and building FAISS index...\n")
            os.system("python ingest_data.py")
            input("\nPress Enter to continue...")

        elif choice == "2":
            print("\n💬 Starting RAG Question Answering...\n")
            os.system("python query_interface.py")
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("\n🚀 Running Gemini RAG Demo...\n")
            os.system("python demo_standalone.py")
            input("\nPress Enter to continue...")

        elif choice == "4":
            check_status()

        elif choice == "5":
            view_docs()

        elif choice == "6":
            print("\n👋 Exiting Helix RAG System\n")
            break

        else:
            print("\n❌ Invalid choice. Try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exited safely\n")
        sys.exit(0)
