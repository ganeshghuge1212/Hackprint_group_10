"""
RAG System Main Module
-----------------------
Hybrid RAG system using:
- MongoDB for structured data
- FAISS for vector search
- MiniLM for embeddings
- Gemini 1.5 Flash for response generation
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from database_handler import MongoDBHandler
from data_loader import DataLoader
from embedding_generator import EmbeddingGenerator, DocumentEmbedder
from faiss_vector_store import MultiIndexManager
from llm_interface import GeminiLLMInterface, PromptBuilder, ResponseFormatter
import config

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class HybridRAGSystem:
    """
    Hybrid RAG system combining structured queries and semantic search.
    """

    def __init__(
        self,
        mongodb_uri: str,
        database_name: str,
        gemini_api_key: str
    ):
        """
        Initialize the RAG system.
        """
        logger.info("Initializing Hybrid RAG System (Gemini 1.5 Flash)...")

        if not gemini_api_key:
            raise ValueError(
                "❌ GEMINI_API_KEY is missing. Set it in environment variables or .env file."
            )

        # MongoDB
        self.db = MongoDBHandler(mongodb_uri, database_name)

        # Data loader
        self.data_loader = DataLoader()

        # Embeddings
        self.embedding_gen = EmbeddingGenerator(config.EMBEDDING_MODEL)
        self.doc_embedder = DocumentEmbedder(self.embedding_gen)

        # Gemini LLM
        self.llm = GeminiLLMInterface(
            api_key=gemini_api_key,
            model_name=config.LLM_MODEL  # gemini-1.5-flash
        )

        # FAISS Indexes
        embedding_dim = self.embedding_gen.get_embedding_dimension()
        self.index_manager = MultiIndexManager(embedding_dim)

        self.employee_index = self.index_manager.create_index("employees")
        self.attendance_index = self.index_manager.create_index("attendance")
        self.leave_index = self.index_manager.create_index("leave")

        self.policy_text = ""

        logger.info("✅ RAG System initialized successfully")

    # ------------------------------------------------------------------
    # DATA LOADING & INDEXING
    # ------------------------------------------------------------------

    def load_and_index_data(
        self,
        employee_csv: str,
        attendance_json: str,
        leave_excel: str,
        policy_pdf: str = None
    ) -> None:

        logger.info("STEP 1: Loading data")

        # Load structured data
        employees = self.data_loader.load_helix_employee_data(employee_csv)
        attendance = self.data_loader.load_helix_attendance_data(attendance_json)
        leave_data = self.data_loader.load_helix_leave_data(leave_excel)
        leave_history = leave_data["history"]
        leave_balances = leave_data["balances"]

        # Load policy PDF if provided
        if policy_pdf:
            self.policy_text = self.data_loader.extract_text_from_pdf(policy_pdf)

        logger.info("STEP 2: Storing data in MongoDB")

        # Employees
        self.db.clear_collection(config.COLLECTIONS["employees"])
        self.db.insert_documents(config.COLLECTIONS["employees"], employees)
        self.db.create_index(config.COLLECTIONS["employees"], "emp_id", unique=True)

        # Attendance
        self.db.clear_collection(config.COLLECTIONS["attendance"])
        self.db.insert_documents(config.COLLECTIONS["attendance"], attendance)

        # Leave History
        self.db.clear_collection(config.COLLECTIONS["leave_history"])
        self.db.insert_documents(config.COLLECTIONS["leave_history"], leave_history)

        # Leave Balances
        self.db.clear_collection(config.COLLECTIONS["leave_balances"])
        self.db.insert_documents(config.COLLECTIONS["leave_balances"], leave_balances)

        logger.info("STEP 3: Generating embeddings")

        # Clear FAISS indexes before adding new vectors
        self.employee_index.clear()
        self.attendance_index.clear()
        self.leave_index.clear()

        # Employee embeddings
        emp_embeddings = self.doc_embedder.embed_employee_records(employees)
        self.employee_index.add_documents(emp_embeddings)

        # Attendance embeddings (limit to 10k for performance)
        attendance_sample = attendance[:10000] if len(attendance) > 10000 else attendance
        att_embeddings = self.doc_embedder.embed_attendance_records(attendance_sample)
        self.attendance_index.add_documents(att_embeddings)

        # Leave embeddings
        leave_embeddings = self.doc_embedder.embed_leave_records(leave_history)
        self.leave_index.add_documents(leave_embeddings)

        self._print_summary()

    def _print_summary(self) -> None:
        print("\n📊 DATA SUMMARY")
        print("Employees:", self.db.count_documents(config.COLLECTIONS["employees"]))
        print("Attendance:", self.db.count_documents(config.COLLECTIONS["attendance"]))
        print("Leave History:", self.db.count_documents(config.COLLECTIONS["leave_history"]))
        print("Leave Balances:", self.db.count_documents(config.COLLECTIONS["leave_balances"]))

    # ------------------------------------------------------------------
    # QUERYING
    # ------------------------------------------------------------------

    def query_semantic(
        self,
        query_text: str,
        index_name: str = "all",
        k: int = 5
    ) -> List[Tuple[Dict, float]]:

        query_vector = self.embedding_gen.generate_embedding(query_text)

        if index_name == "all":
            results = []
            for name in ["employees", "attendance", "leave"]:
                idx = self.index_manager.get_index(name)
                results.extend(idx.search(query_vector, k))
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:k]

        idx = self.index_manager.get_index(index_name)
        return idx.search(query_vector, k)

    def query(self, query_text: str, use_structured: bool = True) -> Dict[str, Any]:

        logger.info(f"Processing query: {query_text}")

        results = []
        search_method = "semantic"

        # Structured query first
        if use_structured:
            structured = self._try_structured_query(query_text)
            if structured:
                results = structured
                search_method = "structured"

        # Semantic fallback
        if not results:
            semantic_results = self.query_semantic(
                query_text,
                k=config.TOP_K_RESULTS
            )
            results = [
                (doc, sim) for doc, sim in semantic_results
                if sim >= config.SIMILARITY_THRESHOLD
            ]

        if not results:
            return {
                "answer": "No relevant information found. Please rephrase your question.",
                "confidence": 0.0,
                "sources": [],
                "search_method": search_method
            }

        if isinstance(results[0], tuple):
            docs = [d for d, _ in results]
            confidence = float(np.mean([s for _, s in results]))
        else:
            docs = results
            confidence = 0.9  # structured queries are more reliable

        prompt = PromptBuilder.build_hr_query_prompt(
            query_text,
            docs,
            policy_context=self.policy_text[:2000]
        )

        answer = self.llm.generate_response(
            prompt,
            temperature=0.3,
            max_tokens=800
        )

        response = ResponseFormatter.format_response(
            answer,
            docs,
            confidence
        )
        response["search_method"] = search_method

        return response

    # ------------------------------------------------------------------
    # STRUCTURED QUERY
    # ------------------------------------------------------------------

    def _try_structured_query(self, query_text: str) -> Optional[List[Dict]]:

        import re
        q = query_text.lower()
        match = re.search(r"emp\d+", q)

        if match:
            emp_id = match.group(0).upper()
            doc = self.db.find_one(
                config.COLLECTIONS["employees"],
                {"emp_id": emp_id}
            )
            return [doc] if doc else None

        return None

    # ------------------------------------------------------------------
    # FAISS SAVE / LOAD
    # ------------------------------------------------------------------

    def save_indexes(self, base_path: str = config.FAISS_INDEX_PATH) -> None:
        self.index_manager.save_all(base_path)

    def load_indexes(self, base_path: str = config.FAISS_INDEX_PATH) -> None:
        self.index_manager.load_all(
            base_path,
            ["employees", "attendance", "leave"]
        )
        self.employee_index = self.index_manager.get_index("employees")
        self.attendance_index = self.index_manager.get_index("attendance")
        self.leave_index = self.index_manager.get_index("leave")

    # ------------------------------------------------------------------
    # CLOSE CONNECTION
    # ------------------------------------------------------------------

    def close(self) -> None:
        self.db.close()
