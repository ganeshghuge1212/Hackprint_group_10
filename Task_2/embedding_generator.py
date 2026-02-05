"""
Embedding Generator Module
---------------------------
This module handles generating vector embeddings using sentence transformers.
Uses "all-MiniLM-L6-v2" model which is lightweight and efficient.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union, Dict, Any
import logging
import torch

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Generates vector embeddings from text using sentence transformers.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence transformer model
        """
        try:
            logger.info(f"Loading embedding model: {model_name}")
            
            # Set device (GPU if available, else CPU)
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            
            self.model = SentenceTransformer(model_name, device=self.device)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            
            logger.info(f"✓ Loaded embedding model on {self.device}")
            logger.info(f"  Embedding dimension: {self.embedding_dim}")
        except Exception as e:
            logger.error(f"✗ Error loading embedding model: {e}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        try:
            # Handle empty or None text
            if not text or not isinstance(text, str):
                text = ""
            
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"✗ Error generating embedding: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process at once
            
        Returns:
            Array of embedding vectors
        """
        try:
            # Handle empty or None texts
            clean_texts = [str(text) if text else "" for text in texts]
            
            logger.info(f"Generating embeddings for {len(clean_texts)} texts...")
            embeddings = self.model.encode(
                clean_texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=True
            )
            logger.info(f"✓ Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"✗ Error generating embeddings: {e}")
            raise
    
    def document_to_text(self, document: Dict[str, Any]) -> str:
        """
        Convert a document to a text representation for embedding.
        Combines all relevant fields into a single text string.
        
        Args:
            document: Document dictionary
            
        Returns:
            Text representation of the document
        """
        text_parts = []
        
        # Fields to exclude from text representation
        exclude_fields = ['_id', 'embedding', 'metadata']
        
        for key, value in document.items():
            if key in exclude_fields:
                continue
            
            # Convert value to string
            if value is None:
                continue
            elif isinstance(value, (list, dict)):
                value_str = str(value)
            else:
                value_str = str(value)
            
            # Add field and value to text
            text_parts.append(f"{key}: {value_str}")
        
        return " | ".join(text_parts)
    
    def embed_documents(self, documents: List[Dict[str, Any]], 
                       text_field: str = None) -> List[Dict[str, Any]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            documents: List of documents to embed
            text_field: Specific field to use for embedding (None uses all fields)
            
        Returns:
            Documents with added 'embedding' field
        """
        try:
            # Extract or create text representations
            if text_field and all(text_field in doc for doc in documents):
                texts = [str(doc[text_field]) for doc in documents]
            else:
                texts = [self.document_to_text(doc) for doc in documents]
            
            # Generate embeddings
            embeddings = self.generate_embeddings(texts)
            
            # Add embeddings to documents
            for doc, embedding in zip(documents, embeddings):
                doc['embedding'] = embedding.tolist()  # Convert to list for JSON serialization
                doc['embedding_text'] = texts[documents.index(doc)]  # Store original text
            
            logger.info(f"✓ Added embeddings to {len(documents)} documents")
            return documents
        except Exception as e:
            logger.error(f"✗ Error embedding documents: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings.
        
        Returns:
            Embedding dimension
        """
        return self.embedding_dim
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1)
        """
        try:
            # Normalize vectors
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Compute cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"✗ Error computing similarity: {e}")
            return 0.0


class DocumentEmbedder:
    """
    Helper class for embedding specific document types with custom logic.
    """
    
    def __init__(self, embedding_generator: EmbeddingGenerator):
        """
        Initialize with an embedding generator.
        
        Args:
            embedding_generator: EmbeddingGenerator instance
        """
        self.embedder = embedding_generator
    
    def embed_employee_records(self, employees: List[Dict]) -> List[Dict]:
        """
        Embed employee records with custom text representation.
        
        Args:
            employees: List of employee documents
            
        Returns:
            Employees with embeddings
        """
        texts = []
        for emp in employees:
            # Create rich text representation
            parts = [
                f"Employee ID: {emp.get('emp_id', '')}",
                f"Name: {emp.get('name', '')}",
                f"Department: {emp.get('dept', '')}",
                f"Location: {emp.get('location', '')}",
                f"Role: {emp.get('role', '')}",
                f"Joining Date: {emp.get('joining_date', '')}",
                f"Performance: {emp.get('performance_rating', '')}",
                f"Certifications: {emp.get('certifications', '')}",
            ]
            texts.append(" | ".join(parts))
        
        embeddings = self.embedder.generate_embeddings(texts)
        
        for emp, embedding, text in zip(employees, embeddings, texts):
            emp['embedding'] = embedding.tolist()
            emp['embedding_text'] = text
        
        return employees
    
    def embed_attendance_records(self, records: List[Dict]) -> List[Dict]:
        """
        Embed attendance records with custom text representation.
        
        Args:
            records: List of attendance documents
            
        Returns:
            Records with embeddings
        """
        texts = []
        for rec in records:
            # Create text representation
            parts = [
                f"Employee: {rec.get('emp_id', '')}",
                f"Date: {rec.get('date', '')}",
                f"Check In: {rec.get('check_in', 'N/A')}",
                f"Check Out: {rec.get('check_out', 'N/A')}",
                f"Location: {rec.get('location_logged', '')}",
                f"Device: {rec.get('device', '')}",
            ]
            texts.append(" | ".join(parts))
        
        embeddings = self.embedder.generate_embeddings(texts)
        
        for rec, embedding, text in zip(records, embeddings, texts):
            rec['embedding'] = embedding.tolist()
            rec['embedding_text'] = text
        
        return records
    
    def embed_leave_records(self, records: List[Dict]) -> List[Dict]:
        """
        Embed leave records with custom text representation.
        
        Args:
            records: List of leave documents
            
        Returns:
            Records with embeddings
        """
        texts = []
        for rec in records:
            # Create text representation
            parts = [
                f"Employee: {rec.get('emp_id', '')}",
                f"Leave Type: {rec.get('leave_type', '')}",
                f"Start Date: {rec.get('start_date', '')}",
                f"End Date: {rec.get('end_date', '')}",
                f"Duration: {rec.get('days', '')} days",
                f"Status: {rec.get('status', '')}",
                f"Reason: {rec.get('reason', '')}",
            ]
            texts.append(" | ".join(parts))
        
        embeddings = self.embedder.generate_embeddings(texts)
        
        for rec, embedding, text in zip(records, embeddings, texts):
            rec['embedding'] = embedding.tolist()
            rec['embedding_text'] = text
        
        return records
