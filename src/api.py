from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

# imports for your 4 concrete classes + RAGPipeline go here
from .chunking.langchain_chunker import LangChainChunker
from .embedding.nvidia_embedder import NvidiaEmbedder
from .vectorstore.database import QdrantVectorStore
from .llm.nvidia_llm import NvidiaLLMClient
from .pipeline import RAGPipeline

pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline
    pipeline = RAGPipeline(
        chunker=LangChainChunker(),
        embedder=NvidiaEmbedder(),
        vector_store=QdrantVectorStore(host="qdrant"),
        llm_client=NvidiaLLMClient()
    )
    yield

app = FastAPI(lifespan=lifespan)

class IngestRequest(BaseModel):
    document: str

class QueryRequest(BaseModel):
    question: str

@app.post("/ingest")
def ingest(request: IngestRequest):
    pipeline.ingest(request.document)
    return {"status": "ingested successfully"}

@app.post("/query")
def query(request: QueryRequest):
    ans=pipeline.query(request.question)
    return {"Answer": ans}