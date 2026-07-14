from abc import ABC,abstractmethod

class Docparse (ABC):
    @abstractmethod
    def parse(self,path:str):
        """This is used to parse the document"""
        pass
