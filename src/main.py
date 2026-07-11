from dotenv import load_dotenv
load_dotenv()

from chunking.langchain_chunker import LangChainChunker
from embedding.nvidia_embedder import NvidiaEmbedder
from vectorstore.database import QdrantVectorStore
from llm.nvidia_llm import NvidiaLLMClient
from pipeline import RAGPipeline

pipeline = RAGPipeline(
    chunker=LangChainChunker(),
    embedder=NvidiaEmbedder(),
    vector_store=QdrantVectorStore(),
    llm_client=NvidiaLLMClient()
)

document = """
The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.
It was designed by engineer Gustave Eiffel and completed in 1889 for the World's Fair.
The tower stands 330 meters tall and was the tallest man-made structure in the world
until 1930. It is now one of the most visited paid monuments in the world.
"""

pipeline.ingest(document)

answer = pipeline.query("How tall is the Eiffel Tower and who designed it?")
print(answer)