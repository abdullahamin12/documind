from abc import ABC, abstractmethod

class Embedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Every embedder MUST implement this. No exceptions."""
        pass