from langchain_text_splitters import RecursiveCharacterTextSplitter
from .base import Chunker

class LangChainChunker(Chunker):
    def chunk(self, text: str, chunk_size: int) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size * 0.1)  # 10% overlap, standard practice
        )
        return splitter.split_text(text)