import os
import requests
from .base import LLMClient

class NvidiaLLMClient(LLMClient):
    def __init__(self, model: str = "mistralai/ministral-14b-instruct-2512"):
        self.api_key = os.environ["NVIDIA_API_KEY2"]
        self.model = model
        self.url = "https://integrate.api.nvidia.com/v1/chat/completions"

    def response(self, context: list[str], question: str) -> str:
        context_text = "\n".join(context)
        prompt = f"""Answer the question using only the context below.

Context:
{context_text}

Question:
{question}"""

        headers = {
            "Authorization": self.api_key,
            "Accept": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
            "temperature": 0.15,
            "top_p": 1.00,
            "frequency_penalty": 0.00,
            "presence_penalty": 0.00,
            "stream": True
        }

        result = requests.post(self.url, headers=headers, json=payload)
        result.raise_for_status()
        return result.json()["choices"][0]["message"]["content"]