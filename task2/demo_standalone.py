"""
Standalone Demo Script
-----------------------
A simplified demo that works without MongoDB for quick testing.
This uses in-memory storage instead of MongoDB.
"""

import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from groq import Groq

# Simple configuration
GROQ_API_KEY = ""  # Add your key here or it will be read from file
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class SimplifiedRAGDemo:
    """
    Simplified RAG system for demonstration without MongoDB.
    """
    
    def __init__(self, api_key):
        print("🚀 Initializing Simplified RAG Demo...")
        
        # Load embedding model
        print("📥 Loading embedding model...")
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        
        # Initialize LLM
        self.llm = Groq(api_key=api_key)
        
        # In-memory storage
        self.employees = []
        self.embeddings = None
        
        print("✅ System ready!")
    
    def load_data(self, csv_path):
        """Load employee data from CSV."""
        print(f"\n📂 Loading data from {csv_path}...")
        
        df = pd.read_csv(csv_path)
        self.employees = df.to_dict('records')
        
        # Create text representations
        texts = []
        for emp in self.employees:
            text = f"Employee {emp.get('emp_id', '')}: {emp.get('name', '')} works in {emp.get('dept', '')} at {emp.get('location', '')} as {emp.get('role', '')}"
            texts.append(text)
        
        # Generate embeddings
        print("🔄 Generating embeddings...")
        self.embeddings = self.embedder.encode(texts, show_progress_bar=True)
        
        print(f"✅ Loaded {len(self.employees)} employees")
    
    def search(self, query, k=3):
        """Search for relevant employees."""
        # Embed query
        query_embedding = self.embedder.encode([query])[0]
        
        # Compute similarities
        similarities = np.dot(self.embeddings, query_embedding)
        
        # Get top k results
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'employee': self.employees[idx],
                'similarity': float(similarities[idx])
            })
        
        return results
    
    def query(self, question):
        """Answer a question using RAG."""
        print(f"\n🔍 Processing query: {question}")
        
        # Search for relevant data
        results = self.search(question, k=3)
        
        # Build context
        context = "Relevant Employee Information:\n\n"
        for i, res in enumerate(results, 1):
            emp = res['employee']
            context += f"{i}. {emp.get('name', 'Unknown')} (ID: {emp.get('emp_id', '')})\n"
            context += f"   Department: {emp.get('dept', '')}\n"
            context += f"   Location: {emp.get('location', '')}\n"
            context += f"   Role: {emp.get('role', '')}\n\n"
        
        # Build prompt
        prompt = f"""You are an HR assistant. Answer the question based on the provided employee data.

{context}

Question: {question}

Provide a clear, concise answer based on the information above.

Answer:"""
        
        # Get LLM response
        print("🤖 Generating answer...")
        response = self.llm.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        answer = response.choices[0].message.content
        
        return {
            'answer': answer,
            'sources': results,
            'confidence': np.mean([r['similarity'] for r in results])
        }
    
    def print_response(self, response):
        """Pretty print response."""
        print("\n" + "="*70)
        print("📝 ANSWER:")
        print("="*70)
        print(response['answer'])
        
        print("\n" + "-"*70)
        print(f"📊 Confidence: {response['confidence']:.2%}")
        print(f"📚 Sources: {len(response['sources'])}")
        
        print("\n" + "-"*70)
        print("🔗 Top Sources:")
        for i, src in enumerate(response['sources'], 1):
            emp = src['employee']
            print(f"{i}. {emp.get('name')} ({emp.get('emp_id')}) - {emp.get('dept')}")
            print(f"   Similarity: {src['similarity']:.2%}")
        
        print("="*70)


def main():
    """Main demo function."""
    print("\n" + "="*70)
    print("  SIMPLIFIED RAG DEMO (No MongoDB Required)")
    print("="*70)
    
    # Get API key
    try:
        with open('/mnt/user-data/uploads/1770275466020_groq_api_key.txt', 'r') as f:
            api_key = f.readline().split(': ')[1].strip()
    except:
        api_key = input("\nEnter your Groq API key: ").strip()
        if not api_key:
            print("❌ API key required!")
            return
    
    # Initialize demo
    demo = SimplifiedRAGDemo(api_key)
    
    # Load data
    csv_path = '/mnt/user-data/uploads/1770275466020_employee_master.csv'
    demo.load_data(csv_path)
    
    # Example queries
    print("\n" + "="*70)
    print("  DEMO QUERIES")
    print("="*70)
    
    queries = [
        "Who works in the Engineering department?",
        "Find employees in Singapore",
        "Who is employee EMP1005?"
    ]
    
    for query in queries:
        response = demo.query(query)
        demo.print_response(response)
        
        proceed = input("\n➡️  Continue to next query? (y/n): ")
        if proceed.lower() != 'y':
            break
    
    # Interactive mode
    print("\n" + "="*70)
    print("  INTERACTIVE MODE")
    print("="*70)
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("💬 Your question: ").strip()
        
        if query.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        try:
            response = demo.query(query)
            demo.print_response(response)
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
