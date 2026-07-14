from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def response(self, context: list[str], question: str, chat_history: list[dict] = None) -> str:
        """Generate an answer grounded in the given context and prior chat history."""
        pass