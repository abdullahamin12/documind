from abc import ABC,abstractmethod
class Chunker(ABC):
    @abstractmethod
    def chunk(self,text:str,chunk_size:int,chunk_overlap:int)->list:
            """"makes chunks"""
            pass