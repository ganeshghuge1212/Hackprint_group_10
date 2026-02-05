"""
LLM Interface Module
--------------------
This module handles interactions with the Groq API for Gemma LLM.
Groq provides fast inference for various open-source models including Gemma.
"""

from groq import Groq
import logging
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class GroqLLMInterface:
    """
    Interface for Groq API to use Gemma LLM for response generation.
    """
    
    def __init__(self, api_key: str, model: str = "gemma2-9b-it"):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key
            model: Model name (default: gemma2-9b-it)
        """
        if not api_key:
            raise ValueError("Groq API key is required")
        
        try:
            self.client = Groq(api_key=api_key)
            self.model = model
            logger.info(f"✓ Initialized Groq client with model: {model}")
        except Exception as e:
            logger.error(f"✗ Error initializing Groq client: {e}")
            raise
    
    def generate_response(self, 
                         prompt: str, 
                         max_tokens: int = 1000,
                         temperature: float = 0.7) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-2)
            
        Returns:
            Generated response text
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            response = completion.choices[0].message.content
            logger.info(f"✓ Generated response ({len(response)} characters)")
            return response
        except Exception as e:
            logger.error(f"✗ Error generating response: {e}")
            raise
    
    def generate_with_context(self,
                             query: str,
                             context: str,
                             max_tokens: int = 1000) -> str:
        """
        Generate response with provided context (for RAG).
        
        Args:
            query: User query
            context: Retrieved context from vector store
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        prompt = f"""You are a helpful HR assistant for Helix Global Corp. Answer the question based on the provided context.

Context:
{context}

Question: {query}

Instructions:
- Provide a clear, accurate answer based on the context
- If the context doesn't contain enough information, say so
- Cite specific details from the context when relevant
- Be concise but complete

Answer:"""
        
        return self.generate_response(prompt, max_tokens=max_tokens, temperature=0.3)
    
    def generate_with_system_prompt(self,
                                   query: str,
                                   context: str,
                                   system_prompt: str,
                                   max_tokens: int = 1000) -> str:
        """
        Generate response with custom system prompt.
        
        Args:
            query: User query
            context: Retrieved context
            system_prompt: Custom system prompt
            max_tokens: Maximum tokens
            
        Returns:
            Generated response
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {query}"
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.3,
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"✗ Error generating response: {e}")
            raise


class PromptBuilder:
    """
    Helper class for building effective RAG prompts.
    """
    
    @staticmethod
    def build_hr_query_prompt(query: str, 
                             retrieved_docs: List[Dict[str, Any]],
                             policy_context: str = "") -> str:
        """
        Build prompt for HR queries.
        
        Args:
            query: User query
            retrieved_docs: Documents retrieved from vector store
            policy_context: Additional policy context
            
        Returns:
            Formatted prompt
        """
        # Format retrieved documents
        context_parts = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            doc_text = f"--- Document {i} ---\n"
            
            # Format document based on type
            if 'emp_id' in doc:
                if 'name' in doc:  # Employee record
                    doc_text += f"Employee: {doc.get('name')} (ID: {doc.get('emp_id')})\n"
                    doc_text += f"Department: {doc.get('dept', 'N/A')}\n"
                    doc_text += f"Location: {doc.get('location', 'N/A')}\n"
                    doc_text += f"Role: {doc.get('role', 'N/A')}\n"
                    doc_text += f"Joining Date: {doc.get('joining_date', 'N/A')}\n"
                elif 'date' in doc:  # Attendance record
                    doc_text += f"Employee ID: {doc.get('emp_id')}\n"
                    doc_text += f"Date: {doc.get('date', 'N/A')}\n"
                    doc_text += f"Check In: {doc.get('check_in', 'N/A')}\n"
                    doc_text += f"Check Out: {doc.get('check_out', 'N/A')}\n"
                elif 'leave_type' in doc:  # Leave record
                    doc_text += f"Employee ID: {doc.get('emp_id')}\n"
                    doc_text += f"Leave Type: {doc.get('leave_type', 'N/A')}\n"
                    doc_text += f"Duration: {doc.get('days', 'N/A')} days\n"
                    doc_text += f"Status: {doc.get('status', 'N/A')}\n"
            
            # Add embedding text if available
            if 'embedding_text' in doc:
                doc_text += f"\nFull Details: {doc['embedding_text']}\n"
            
            context_parts.append(doc_text)
        
        context = "\n".join(context_parts)
        
        # Add policy context if provided
        if policy_context:
            context = f"HR POLICIES:\n{policy_context}\n\nRELEVANT DATA:\n{context}"
        
        prompt = f"""You are an intelligent HR assistant for Helix Global Corp. Answer the following question based on the provided context.

{context}

Question: {query}

Instructions:
- Provide a clear, accurate, and professional answer
- Base your answer strictly on the provided context
- If you reference specific data, mention which document it came from
- If the context doesn't contain enough information, clearly state what's missing
- For policy questions, cite the specific policy sections
- For employee data questions, provide specific details from the records

Answer:"""
        
        return prompt
    
    @staticmethod
    def build_analytical_prompt(query: str, 
                               data_summary: Dict[str, Any]) -> str:
        """
        Build prompt for analytical queries.
        
        Args:
            query: User query
            data_summary: Summary statistics from database
            
        Returns:
            Formatted prompt
        """
        summary_text = json.dumps(data_summary, indent=2)
        
        prompt = f"""You are a data analyst for Helix Global Corp HR department. Analyze the following data and answer the question.

DATA SUMMARY:
{summary_text}

Question: {query}

Instructions:
- Provide insights based on the data
- Use specific numbers and statistics
- Identify trends or patterns
- Make data-driven recommendations if appropriate

Answer:"""
        
        return prompt


class ResponseFormatter:
    """
    Helper class for formatting LLM responses with metadata.
    """
    
    @staticmethod
    def format_response(response_text: str,
                       sources: List[Dict[str, Any]],
                       confidence: float) -> Dict[str, Any]:
        """
        Format response with metadata.
        
        Args:
            response_text: Generated response
            sources: Source documents used
            confidence: Confidence score
            
        Returns:
            Formatted response dictionary
        """
        return {
            "answer": response_text,
            "confidence": confidence,
            "sources": sources,
            "source_count": len(sources),
            "metadata": {
                "has_sources": len(sources) > 0,
                "confidence_level": "high" if confidence > 0.7 else "medium" if confidence > 0.5 else "low"
            }
        }
    
    @staticmethod
    def format_source_references(sources: List[Dict[str, Any]]) -> str:
        """
        Format source references for display.
        
        Args:
            sources: Source documents
            
        Returns:
            Formatted reference text
        """
        if not sources:
            return "No source documents found."
        
        refs = ["Sources:"]
        for i, source in enumerate(sources, 1):
            ref = f"{i}. "
            
            if 'emp_id' in source:
                ref += f"Employee {source.get('emp_id', 'Unknown')}"
                if 'name' in source:
                    ref += f" ({source.get('name')})"
            elif 'embedding_text' in source:
                # Show first 100 characters
                text = source['embedding_text'][:100]
                ref += f"{text}..."
            
            refs.append(ref)
        
        return "\n".join(refs)
