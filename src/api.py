
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

# RAG Pipeline Imports
from .chunking.langchain_chunker import LangChainChunker
from .embedding.nvidia_embedder import NvidiaEmbedder
from .vectorstore.database import QdrantVectorStore
from .llm.nvidia_llm import NvidiaLLMClient
from .pipeline import RAGPipeline

# History and Parser Imports
from .chat_history.chat import PostgresChatHistory

pipeline = None
db_repo = None 

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline
    global db_repo
    
    # Instantiate the database connection
    db_repo = PostgresChatHistory(
        host="postgres", 
        database="documind", 
        user="myuser", 
        password="123"
    )
    
    # Initialize the RAG Pipeline
    pipeline = RAGPipeline(
        chunker=LangChainChunker(),
        embedder=NvidiaEmbedder(),
        vector_store=QdrantVectorStore(host="qdrant"),
        llm_client=NvidiaLLMClient()
    )
    yield

app = FastAPI(lifespan=lifespan)

# ---------------------------------------------------------
# PYDANTIC MODELS (Strictly for JSON payloads)
# ---------------------------------------------------------
class IngestRequest(BaseModel):
    document: str

class QueryRequest(BaseModel):
    question: str

# ---------------------------------------------------------
# ENDPOINT 1: Raw Text Ingestion
# ---------------------------------------------------------
@app.post("/ingest/text")
def ingest_text(request: IngestRequest):
    pipeline.ingest(request.document)
    return {"status": "Raw text ingested successfully"}

# ---------------------------------------------------------
# ENDPOINT 2: PDF File Ingestion
# ---------------------------------------------------------

# ---------------------------------------------------------
# ENDPOINT 3: Query Generation
# ---------------------------------------------------------
@app.post("/query")
def query(request: QueryRequest):
    # EXTRACT: Pull the last 5 messages from PostgreSQL
    history = db_repo.extract_history(limit=5)
    
    # QUERY: Pass the question AND the history to the pipeline
    ans = pipeline.query(request.question, chat_history=history)
    
    # SAVE: Store the new interaction
    db_repo.save_history(request.question, ans)
    
    return {"Answer": ans}