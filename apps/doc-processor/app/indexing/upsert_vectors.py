import os, time
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "financial-docs")

def upsert_pinecone(items: List[Dict[str, Any]]):
    """
    items: [{ "id": str, "values": [floats], "metadata": {...} }, ...]
    """
    if not PINECONE_API_KEY:
        raise RuntimeError("PINECONE_API_KEY no definido.")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Crear índice si no existe (dimension = len del primer vector)
    dim = len(items[0]["values"])
    exists = any(i.name == PINECONE_INDEX for i in pc.list_indexes())
    if not exists:
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=dim,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while pc.describe_index(PINECONE_INDEX).status["ready"] is False:
            time.sleep(2)

    index = pc.Index(PINECONE_INDEX)
    for i in range(0, len(items), 100):
        batch = items[i:i+100]
        index.upsert(vectors=batch)
