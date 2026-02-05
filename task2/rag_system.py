"""
RAG System Main Module
-----------------------
This is the main RAG system that orchestrates all components:
- MongoDB for structured data storage
- FAISS for vector similarity search
- Mini LLM for embeddings
- Gemma LLM for response generation
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime

from database_handler import MongoDBHandler
from data_loader import DataLoader
from embedding_generator import EmbeddingGenerator, DocumentEmbedder
from faiss_vector_store import FAISSVectorStore, MultiIndexManager
from llm_interface import GroqLLMInterface, PromptBuilder, ResponseFormatter
import config

logger = logging.getLogger(__name__)


class HybridRAGSystem:
    """
    Hybrid RAG system combining structured queries and vector search.
    """
    
    def __init__(self, 
                 mongodb_uri: str,
                 database_name: str,
                 groq_api_key: str):
        """
        Initialize the RAG system.
        
        Args:
            mongodb_uri: MongoDB connection string
            database_name: Name of the database
            groq_api_key: Groq API key for LLM
        """
        logger.info("Initializing Hybrid RAG System...")
        
        # Initialize components
        self.db = MongoDBHandler(mongodb_uri, database_name)
        self.data_loader = DataLoader()
        self.embedding_gen = EmbeddingGenerator(config.EMBEDDING_MODEL)
        self.doc_embedder = DocumentEmbedder(self.embedding_gen)
        self.llm = GroqLLMInterface(groq_api_key, config.LLM_MODEL)
        
        # Initialize multi-index manager
        embedding_dim = self.embedding_gen.get_embedding_dimension()
        self.index_manager = MultiIndexManager(embedding_dim)
        
        # Create indexes for different document types
        self.employee_index = self.index_manager.create_index("employees")
        self.attendance_index = self.index_manager.create_index("attendance")
        self.leave_index = self.index_manager.create_index("leave")
        
        # Policy text storage (for reference)
        self.policy_text = ""
        
        logger.info("✓ RAG System initialized successfully")
    
    def load_and_index_data(self,
                           employee_csv: str,
                           attendance_json: str,
                           leave_excel: str,
                           policy_pdf: str = None) -> None:
        """
        Load all data, store in MongoDB, and create FAISS indexes.
        
        Args:
            employee_csv: Path to employee master CSV
            attendance_json: Path to attendance JSON
            leave_excel: Path to leave intelligence Excel
            policy_pdf: Path to policy PDF (optional)
        """
        logger.info("=" * 60)
        logger.info("STEP 1: Loading Data from Files")
        logger.info("=" * 60)
        
        # 1. Load employee data
        logger.info("\n[1/4] Loading Employee Data...")
        employees = self.data_loader.load_helix_employee_data(employee_csv)
        
        # 2. Load attendance data
        logger.info("\n[2/4] Loading Attendance Data...")
        attendance = self.data_loader.load_helix_attendance_data(attendance_json)
        
        # 3. Load leave data
        logger.info("\n[3/4] Loading Leave Data...")
        leave_data = self.data_loader.load_helix_leave_data(leave_excel)
        leave_history = leave_data['history']
        leave_balances = leave_data['balances']
        
        # 4. Load policy document (if provided)
        if policy_pdf:
            logger.info("\n[4/4] Loading Policy Document...")
            self.policy_text = self.data_loader.extract_text_from_pdf(policy_pdf)
        
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: Storing Data in MongoDB")
        logger.info("=" * 60)
        
        # Store in MongoDB
        logger.info("\n[1/4] Storing Employees...")
        self.db.clear_collection(config.COLLECTIONS['employees'])
        self.db.insert_documents(config.COLLECTIONS['employees'], employees)
        self.db.create_index(config.COLLECTIONS['employees'], 'emp_id', unique=True)
        
        logger.info("\n[2/4] Storing Attendance Records...")
        self.db.clear_collection(config.COLLECTIONS['attendance'])
        self.db.insert_documents(config.COLLECTIONS['attendance'], attendance)
        
        logger.info("\n[3/4] Storing Leave History...")
        self.db.clear_collection(config.COLLECTIONS['leave_history'])
        self.db.insert_documents(config.COLLECTIONS['leave_history'], leave_history)
        
        logger.info("\n[4/4] Storing Leave Balances...")
        self.db.clear_collection(config.COLLECTIONS['leave_balances'])
        self.db.insert_documents(config.COLLECTIONS['leave_balances'], leave_balances)
        
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: Generating Embeddings")
        logger.info("=" * 60)
        
        # Generate embeddings and add to FAISS
        logger.info("\n[1/3] Embedding Employee Records...")
        employees_embedded = self.doc_embedder.embed_employee_records(employees)
        self.employee_index.add_documents(employees_embedded)
        
        logger.info("\n[2/3] Embedding Attendance Records...")
        # Sample attendance to avoid memory issues (take recent records)
        attendance_sample = attendance[:10000] if len(attendance) > 10000 else attendance
        attendance_embedded = self.doc_embedder.embed_attendance_records(attendance_sample)
        self.attendance_index.add_documents(attendance_embedded)
        
        logger.info("\n[3/3] Embedding Leave Records...")
        leave_embedded = self.doc_embedder.embed_leave_records(leave_history)
        self.leave_index.add_documents(leave_embedded)
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ DATA LOADING AND INDEXING COMPLETE")
        logger.info("=" * 60)
        
        # Print summary
        self._print_summary()
    
    def _print_summary(self) -> None:
        """Print summary of loaded data."""
        print("\n📊 DATA SUMMARY:")
        print(f"  Employees: {self.db.count_documents(config.COLLECTIONS['employees'])}")
        print(f"  Attendance Records: {self.db.count_documents(config.COLLECTIONS['attendance'])}")
        print(f"  Leave History: {self.db.count_documents(config.COLLECTIONS['leave_history'])}")
        print(f"  Leave Balances: {self.db.count_documents(config.COLLECTIONS['leave_balances'])}")
        print(f"\n🔍 FAISS INDEXES:")
        print(f"  Employee Index: {self.employee_index.get_stats()['total_vectors']} vectors")
        print(f"  Attendance Index: {self.attendance_index.get_stats()['total_vectors']} vectors")
        print(f"  Leave Index: {self.leave_index.get_stats()['total_vectors']} vectors")
    
    def query_structured(self, collection: str, query: Dict) -> List[Dict]:
        """
        Query MongoDB for exact matches.
        
        Args:
            collection: Collection name
            query: MongoDB query filter
            
        Returns:
            Matching documents
        """
        return self.db.find_documents(collection, query)
    
    def query_semantic(self, 
                      query_text: str, 
                      index_name: str = "all",
                      k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Perform semantic search using FAISS.
        
        Args:
            query_text: Query text
            index_name: Which index to search ('employees', 'attendance', 'leave', 'all')
            k: Number of results
            
        Returns:
            List of (document, similarity_score) tuples
        """
        # Generate query embedding
        query_embedding = self.embedding_gen.generate_embedding(query_text)
        
        if index_name == "all":
            # Search all indexes
            results = []
            for idx_name in ['employees', 'attendance', 'leave']:
                index = self.index_manager.get_index(idx_name)
                idx_results = index.search(query_embedding, k=k)
                results.extend(idx_results)
            
            # Sort by similarity and return top k
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:k]
        else:
            # Search specific index
            index = self.index_manager.get_index(index_name)
            return index.search(query_embedding, k=k)
    
    def query(self, query_text: str, use_structured: bool = True) -> Dict[str, Any]:
        """
        Main query interface - combines structured and semantic search.
        
        Args:
            query_text: User query
            use_structured: Whether to try structured query first
            
        Returns:
            Response dictionary with answer and metadata
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESSING QUERY: {query_text}")
        logger.info(f"{'='*60}")
        
        results = []
        search_method = "hybrid"
        
        # Try structured query first for specific patterns
        if use_structured:
            structured_results = self._try_structured_query(query_text)
            if structured_results:
                results = structured_results
                search_method = "structured"
                logger.info(f"✓ Found {len(results)} results via structured query")
        
        # If no structured results, use semantic search
        if not results:
            semantic_results = self.query_semantic(query_text, index_name="all", k=config.TOP_K_RESULTS)
            
            # Filter by similarity threshold
            results = [(doc, sim) for doc, sim in semantic_results 
                      if sim >= config.SIMILARITY_THRESHOLD]
            search_method = "semantic"
            logger.info(f"✓ Found {len(results)} results via semantic search")
        
        # Generate response using LLM
        if results:
            # Extract documents and similarities
            if isinstance(results[0], tuple):
                docs = [doc for doc, _ in results]
                similarities = [sim for _, sim in results]
                avg_confidence = np.mean(similarities)
            else:
                docs = results
                avg_confidence = 0.8  # Default for structured queries
            
            # Build prompt
            prompt = PromptBuilder.build_hr_query_prompt(
                query_text, 
                docs, 
                policy_context=self.policy_text[:2000] if self.policy_text else ""
            )
            
            # Generate response
            logger.info("🤖 Generating response with LLM...")
            answer = self.llm.generate_response(prompt, max_tokens=800, temperature=0.3)
            
            # Format response
            response = ResponseFormatter.format_response(
                answer,
                docs,
                avg_confidence
            )
            response['search_method'] = search_method
            
        else:
            # No relevant results found
            response = {
                "answer": "I couldn't find relevant information to answer your question. "
                         "Please try rephrasing or ask a more specific question about employees, "
                         "attendance, or leave policies.",
                "confidence": 0.0,
                "sources": [],
                "source_count": 0,
                "search_method": search_method,
                "metadata": {
                    "has_sources": False,
                    "confidence_level": "none"
                }
            }
        
        logger.info(f"✓ Query complete (method: {search_method}, confidence: {response['confidence']:.2f})")
        return response
    
    def _try_structured_query(self, query_text: str) -> Optional[List[Dict]]:
        """
        Attempt to answer query with structured MongoDB query.
        
        Args:
            query_text: User query
            
        Returns:
            Results if matched, None otherwise
        """
        query_lower = query_text.lower()
        
        # Pattern: "employee EMP1234" or "emp id EMP1234"
        if 'emp' in query_lower:
            import re
            emp_id_match = re.search(r'emp\d+', query_lower, re.IGNORECASE)
            if emp_id_match:
                emp_id = emp_id_match.group(0).upper()
                result = self.db.find_one(config.COLLECTIONS['employees'], {'emp_id': emp_id})
                return [result] if result else None
        
        # Pattern: employee name
        if 'employee' in query_lower or 'person' in query_lower:
            # Try to extract name (simple approach)
            words = query_text.split()
            for i, word in enumerate(words):
                if word.lower() in ['employee', 'person', 'named']:
                    if i + 1 < len(words):
                        name = words[i + 1]
                        results = self.db.find_documents(
                            config.COLLECTIONS['employees'],
                            {'name': {'$regex': name, '$options': 'i'}},
                            limit=5
                        )
                        return results if results else None
        
        return None
    
    def save_indexes(self, base_path: str = config.FAISS_INDEX_PATH) -> None:
        """
        Save all FAISS indexes to disk.
        
        Args:
            base_path: Base directory path
        """
        logger.info(f"Saving FAISS indexes to {base_path}...")
        self.index_manager.save_all(base_path)
        logger.info("✓ Indexes saved")
    
    def load_indexes(self, base_path: str = config.FAISS_INDEX_PATH) -> None:
        """
        Load FAISS indexes from disk.
        
        Args:
            base_path: Base directory path
        """
        logger.info(f"Loading FAISS indexes from {base_path}...")
        self.index_manager.load_all(base_path, ['employees', 'attendance', 'leave'])
        
        # Reassign index references
        self.employee_index = self.index_manager.get_index('employees')
        self.attendance_index = self.index_manager.get_index('attendance')
        self.leave_index = self.index_manager.get_index('leave')
        
        logger.info("✓ Indexes loaded")
    
    def close(self) -> None:
        """Close database connection."""
        self.db.close()
