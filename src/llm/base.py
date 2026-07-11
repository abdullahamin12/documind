from abc import ABC,abstractmethod
class LLMClient(ABC):
    @abstractmethod
    def response(self, context: list[str], question: str) -> str:
        """generate an answer grounded in the given context"""
        pass