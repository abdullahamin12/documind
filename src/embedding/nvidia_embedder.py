import os
from typing import Optional
from openai import OpenAI
from .base import Embedder
from dotenv import load_dotenv
load_dotenv()
class NvidiaEmbedder(Embedder):
    def __init__(self, model: str = "nvidia/nv-embed-v1"):
        self.client = OpenAI(
            api_key=os.environ["NVIDIA_API_KEY1"],
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model = model
        

    def embed(self, text: str, input_type: Optional[str] = None) -> list[float]:
        response = self.client.embeddings.create(
            input=[text],
            model=self.model,
            encoding_format="float",
            #if nothing is passed in input type then it is considered as passage 
            extra_body={"input_type": input_type or "passage", "truncate": "NONE"}
        )
        return response.data[0].embedding
