from abc import ABC, abstractmethod
from typing import Optional
class Embedder(ABC):
    @abstractmethod
    def embed(self, text: str,name_type:Optional[str]) -> list[float]:
        """Every embedder MUST implement this. No exceptions."""
        pass