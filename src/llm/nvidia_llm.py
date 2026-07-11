import os
import requests
import json
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
            "Accept": "text/event-stream"
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

        result = requests.post(self.url, headers=headers, json=payload, stream=True)
        result.raise_for_status()

        full_answer = ""
        for line in result.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if decoded == "data: [DONE]":
                break
            if decoded.startswith("data: "):
                chunk = json.loads(decoded[len("data: "):])
                delta = chunk["choices"][0]["delta"].get("content")
                if delta:
                    full_answer += delta

        return full_answer