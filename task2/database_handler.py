"""
MongoDB Database Handler
-------------------------
This module handles all MongoDB operations including:
- Connection management
- Data insertion
- Data retrieval
- Query operations
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MongoDBHandler:
    """
    Handles all interactions with MongoDB database.
    """
    
    def __init__(self, uri: str, database_name: str):
        """
        Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection string
            database_name: Name of the database to use
        """
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            logger.info(f"✓ Connected to MongoDB database: {database_name}")
        except ConnectionFailure as e:
            logger.error(f"✗ Failed to connect to MongoDB: {e}")
            raise
    
    def create_collection(self, collection_name: str) -> None:
        """
        Create a new collection if it doesn't exist.
        
        Args:
            collection_name: Name of the collection
        """
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            logger.info(f"✓ Created collection: {collection_name}")
        else:
            logger.info(f"Collection '{collection_name}' already exists")
    
    def insert_documents(self, collection_name: str, documents: List[Dict]) -> int:
        """
        Insert multiple documents into a collection.
        
        Args:
            collection_name: Name of the collection
            documents: List of documents to insert
            
        Returns:
            Number of documents inserted
        """
        if not documents:
            logger.warning("No documents to insert")
            return 0
        
        try:
            collection = self.db[collection_name]
            result = collection.insert_many(documents, ordered=False)
            count = len(result.inserted_ids)
            logger.info(f"✓ Inserted {count} documents into {collection_name}")
            return count
        except DuplicateKeyError as e:
            logger.warning(f"Some documents already exist: {e}")
            return 0
        except Exception as e:
            logger.error(f"✗ Error inserting documents: {e}")
            raise
    
    def insert_document(self, collection_name: str, document: Dict) -> str:
        """
        Insert a single document into a collection.
        
        Args:
            collection_name: Name of the collection
            document: Document to insert
            
        Returns:
            Inserted document ID
        """
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"✗ Error inserting document: {e}")
            raise
    
    def find_documents(self, 
                      collection_name: str, 
                      query: Dict = None,
                      projection: Dict = None,
                      limit: int = 0) -> List[Dict]:
        """
        Find documents matching a query.
        
        Args:
            collection_name: Name of the collection
            query: MongoDB query filter (None returns all documents)
            projection: Fields to include/exclude
            limit: Maximum number of documents to return (0 = no limit)
            
        Returns:
            List of matching documents
        """
        try:
            collection = self.db[collection_name]
            query = query or {}
            cursor = collection.find(query, projection).limit(limit)
            documents = list(cursor)
            logger.info(f"✓ Found {len(documents)} documents in {collection_name}")
            return documents
        except Exception as e:
            logger.error(f"✗ Error finding documents: {e}")
            raise
    
    def find_one(self, collection_name: str, query: Dict) -> Optional[Dict]:
        """
        Find a single document matching a query.
        
        Args:
            collection_name: Name of the collection
            query: MongoDB query filter
            
        Returns:
            Matching document or None
        """
        try:
            collection = self.db[collection_name]
            document = collection.find_one(query)
            return document
        except Exception as e:
            logger.error(f"✗ Error finding document: {e}")
            raise
    
    def update_document(self, 
                       collection_name: str, 
                       query: Dict, 
                       update: Dict) -> int:
        """
        Update documents matching a query.
        
        Args:
            collection_name: Name of the collection
            query: MongoDB query filter
            update: Update operations
            
        Returns:
            Number of documents modified
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_many(query, update)
            logger.info(f"✓ Modified {result.modified_count} documents")
            return result.modified_count
        except Exception as e:
            logger.error(f"✗ Error updating documents: {e}")
            raise
    
    def delete_documents(self, collection_name: str, query: Dict) -> int:
        """
        Delete documents matching a query.
        
        Args:
            collection_name: Name of the collection
            query: MongoDB query filter
            
        Returns:
            Number of documents deleted
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_many(query)
            logger.info(f"✓ Deleted {result.deleted_count} documents")
            return result.deleted_count
        except Exception as e:
            logger.error(f"✗ Error deleting documents: {e}")
            raise
    
    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """
        Count documents in a collection.
        
        Args:
            collection_name: Name of the collection
            query: MongoDB query filter (None counts all documents)
            
        Returns:
            Number of documents
        """
        try:
            collection = self.db[collection_name]
            query = query or {}
            count = collection.count_documents(query)
            return count
        except Exception as e:
            logger.error(f"✗ Error counting documents: {e}")
            raise
    
    def create_index(self, collection_name: str, field: str, unique: bool = False) -> None:
        """
        Create an index on a field.
        
        Args:
            collection_name: Name of the collection
            field: Field name to index
            unique: Whether the index should enforce uniqueness
        """
        try:
            collection = self.db[collection_name]
            collection.create_index([(field, ASCENDING)], unique=unique)
            logger.info(f"✓ Created index on {collection_name}.{field}")
        except Exception as e:
            logger.error(f"✗ Error creating index: {e}")
            raise
    
    def clear_collection(self, collection_name: str) -> int:
        """
        Remove all documents from a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Number of documents deleted
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_many({})
            logger.info(f"✓ Cleared {result.deleted_count} documents from {collection_name}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"✗ Error clearing collection: {e}")
            raise
    
    def get_collection_stats(self, collection_name: str) -> Dict:
        """
        Get statistics about a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary with collection statistics
        """
        try:
            stats = self.db.command("collStats", collection_name)
            return {
                "count": stats.get("count", 0),
                "size": stats.get("size", 0),
                "avg_document_size": stats.get("avgObjSize", 0)
            }
        except Exception as e:
            logger.error(f"✗ Error getting collection stats: {e}")
            return {}
    
    def close(self) -> None:
        """
        Close the MongoDB connection.
        """
        if self.client:
            self.client.close()
            logger.info("✓ MongoDB connection closed")
