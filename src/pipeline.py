#_____________ALL ABCs______________
from .chunking.base import Chunker
from .embedding.base import Embedder
from .vectorstore.base import VectorStore
from .llm.base import LLMClient


#_______________RAG orchestrator____________________
class RAGPipeline:
    def __init__(self, chunker: Chunker, embedder: Embedder, vector_store: VectorStore, llm_client: LLMClient):
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm_client = llm_client

    def ingest(self, document: str):
        chunks = self.chunker.chunk(document, chunk_size=500)
        for index, chunk_text in enumerate(chunks, start=1):
            vector = self.embedder.embed(chunk_text, input_type="passage")
            self.vector_store.save(vector, index, chunk_text)

    def query(self, question: str) -> str:
        vector = self.embedder.embed(question, input_type="query")
        context = self.vector_store.search(vector, top_k=5)
        return self.llm_client.response(context, question)