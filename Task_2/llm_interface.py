import os

class GeminiLLMInterface:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    def generate_response(self, prompt: str, temperature: float = 0.3, max_tokens: int = 800) -> str:
        # Replace with actual Gemini API call if available
        return f"Simulated response to prompt:\n{prompt}"

class PromptBuilder:
    @staticmethod
    def build_hr_query_prompt(query: str, docs: list, policy_context: str = "") -> str:
        prompt = "You are a helpful HR assistant.\n"
        if policy_context:
            prompt += f"Company Policy:\n{policy_context}\n"
        if docs:
            prompt += "Reference Documents:\n"
            for i, d in enumerate(docs, 1):
                prompt += f"[{i}] {d}\n"
        prompt += f"\nAnswer the question clearly:\n{query}\n"
        return prompt

class ResponseFormatter:
    @staticmethod
    def format_response(answer: str, docs: list, confidence: float) -> dict:
        return {
            "answer": answer,
            "sources": docs,
            "source_count": len(docs),
            "confidence": confidence
        }
