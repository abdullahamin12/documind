from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams, Distance
from .base import VectorStore

class QdrantVectorStore(VectorStore):
    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "documents",vector_size: int = 4096):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
    def save(self, vector: list, id: str, text: str, meta_data: dict = None):
        payload = {"text": text, **(meta_data or {})}
        point = PointStruct(
            id=id,
            vector=vector,
            payload=payload,
            
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def search(self, vector: list, top_k: int) -> list:
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k
        ).points

        ls = []
        for result in results:
            ls.append(result.payload["text"])
        return ls