from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class ChatHistoryRepository(ABC):
    
    @abstractmethod
    def save_history(self, question: str, answer: str, meta_data: Optional[Dict] = None) -> None:
        """
        Saves a question and its corresponding answer to the storage medium.
        """
        pass
    
    @abstractmethod
    def extract_history(self, limit: int = 5) -> List[Dict]:
        """
        Retrieves the most recent conversation history.
        Returns a list of dictionaries containing past questions and answers.
        """
        pass