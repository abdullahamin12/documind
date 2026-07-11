from abc import ABC,abstractmethod
class VectorStore(ABC):
    @abstractmethod
    def save(self, vector: list, id: str, text: str, meta_data: dict = None):
        """save data"""
        pass

    @abstractmethod
    def search(self, vector: list, top_k: int) -> list:
        """search data"""
        pass