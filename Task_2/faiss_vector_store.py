"""
FAISS Vector Store Module
--------------------------
This module handles vector storage and similarity search using FAISS.
FAISS (Facebook AI Similarity Search) is a library for efficient similarity search.
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class FAISSVectorStore:
    """
    Manages FAISS vector index for similarity search.
    """
    
    def __init__(self, dimension: int, index_type: str = "flat"):
        """
        Initialize FAISS index.
        
        Args:
            dimension: Dimension of the embedding vectors
            index_type: Type of FAISS index ('flat' or 'ivf')
                       'flat' = exact search (slower but accurate)
                       'ivf' = approximate search (faster but less accurate)
        """
        self.dimension = dimension
        self.index_type = index_type
        self.documents = []  # Store original documents
        self.index = None
        
        self._create_index()
    
    def _create_index(self) -> None:
        """
        Create FAISS index based on index type.
        """
        try:
            if self.index_type == "flat":
                # Exact search using L2 distance
                self.index = faiss.IndexFlatL2(self.dimension)
                logger.info(f"✓ Created FAISS Flat index (dimension: {self.dimension})")
            elif self.index_type == "ivf":
                # Approximate search using Inverted File Index
                quantizer = faiss.IndexFlatL2(self.dimension)
                n_list = 100  # Number of clusters
                self.index = faiss.IndexIVFFlat(quantizer, self.dimension, n_list)
                logger.info(f"✓ Created FAISS IVF index (dimension: {self.dimension})")
            else:
                raise ValueError(f"Unknown index type: {self.index_type}")
        except Exception as e:
            logger.error(f"✗ Error creating FAISS index: {e}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents with embeddings to the index.
        
        Args:
            documents: List of documents, each containing an 'embedding' field
        """
        try:
            if not documents:
                logger.warning("No documents to add")
                return
            
            # Extract embeddings
            embeddings = []
            for doc in documents:
                if 'embedding' not in doc:
                    raise ValueError("Document missing 'embedding' field")
                embeddings.append(doc['embedding'])
            
            # Convert to numpy array
            embeddings_array = np.array(embeddings).astype('float32')
            
            # If using IVF index, train first
            if self.index_type == "ivf" and not self.index.is_trained:
                logger.info("Training IVF index...")
                self.index.train(embeddings_array)
            
            # Add embeddings to index
            self.index.add(embeddings_array)
            
            # Store original documents
            self.documents.extend(documents)
            
            logger.info(f"✓ Added {len(documents)} documents to FAISS index")
            logger.info(f"  Total documents in index: {self.index.ntotal}")
        except Exception as e:
            logger.error(f"✗ Error adding documents to index: {e}")
            raise
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of tuples (document, similarity)
        """
        try:
            if self.index.ntotal == 0:
                logger.warning("Index is empty")
                return []
            
            # Ensure query is 2D array
            if len(query_embedding.shape) == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            # Convert to float32
            query_embedding = query_embedding.astype('float32')
            
            # Search
            distances, indices = self.index.search(query_embedding, k)
            
            # Prepare results
            results = []
            for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
                if idx < len(self.documents):
                    similarity = 1 / (1 + dist)  # Lower distance → higher similarity
                    results.append((self.documents[idx], similarity))
            
            logger.info(f"✓ Found {len(results)} similar documents")
            return results
        except Exception as e:
            logger.error(f"✗ Error searching index: {e}")
            raise
    
    def search_with_filter(self, 
                          query_embedding: np.ndarray, 
                          k: int = 5,
                          filter_func: callable = None) -> List[Tuple[Dict, float]]:
        """
        Search with post-filtering.
        """
        try:
            initial_k = min(k * 5, self.index.ntotal)
            results = self.search(query_embedding, k=initial_k)
            
            if filter_func:
                results = [(doc, sim) for doc, sim in results if filter_func(doc)]
            
            return results[:k]
        except Exception as e:
            logger.error(f"✗ Error in filtered search: {e}")
            raise
    
    def save(self, index_path: str, documents_path: str) -> None:
        """
        Save FAISS index and documents to disk.
        """
        try:
            os.makedirs(os.path.dirname(index_path) or '.', exist_ok=True)
            os.makedirs(os.path.dirname(documents_path) or '.', exist_ok=True)
            
            faiss.write_index(self.index, index_path)
            
            with open(documents_path, 'wb') as f:
                pickle.dump(self.documents, f)
            
            logger.info(f"✓ Saved FAISS index to {index_path}")
            logger.info(f"✓ Saved documents to {documents_path}")
        except Exception as e:
            logger.error(f"✗ Error saving index: {e}")
            raise
    
    def load(self, index_path: str, documents_path: str) -> None:
        """
        Load FAISS index and documents from disk.
        """
        try:
            self.index = faiss.read_index(index_path)
            
            with open(documents_path, 'rb') as f:
                self.documents = pickle.load(f)
            
            logger.info(f"✓ Loaded FAISS index from {index_path}")
            logger.info(f"✓ Loaded {len(self.documents)} documents")
            logger.info(f"  Index contains {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"✗ Error loading index: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "index_type": self.index_type,
            "is_trained": self.index.is_trained if hasattr(self.index, 'is_trained') else True,
            "total_documents": len(self.documents)
        }
    
    def clear(self) -> None:
        """
        Clear all vectors and documents from the index.
        """
        self.documents = []
        self._create_index()
        logger.info("✓ Cleared index")
    
    # ✅ Added for backward compatibility
    reset = clear


class MultiIndexManager:
    """
    Manages multiple FAISS indexes for different document types.
    """
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.indexes = {}
    
    def create_index(self, name: str, index_type: str = "flat") -> FAISSVectorStore:
        self.indexes[name] = FAISSVectorStore(self.dimension, index_type)
        logger.info(f"✓ Created index: {name}")
        return self.indexes[name]
    
    def get_index(self, name: str) -> FAISSVectorStore:
        if name not in self.indexes:
            raise ValueError(f"Index '{name}' not found")
        return self.indexes[name]
    
    def search_all(self, query_embedding: np.ndarray, k: int = 5) -> Dict[str, List[Tuple[Dict, float]]]:
        results = {}
        for name, index in self.indexes.items():
            results[name] = index.search(query_embedding, k)
        return results
    
    def save_all(self, base_path: str) -> None:
        os.makedirs(base_path, exist_ok=True)
        for name, index in self.indexes.items():
            index_path = os.path.join(base_path, f"{name}_index.faiss")
            docs_path = os.path.join(base_path, f"{name}_docs.pkl")
            index.save(index_path, docs_path)
    
    def load_all(self, base_path: str, index_names: List[str]) -> None:
        for name in index_names:
            index_path = os.path.join(base_path, f"{name}_index.faiss")
            docs_path = os.path.join(base_path, f"{name}_docs.pkl")
            
            if os.path.exists(index_path) and os.path.exists(docs_path):
                index = FAISSVectorStore(self.dimension)
                index.load(index_path, docs_path)
                self.indexes[name] = index
