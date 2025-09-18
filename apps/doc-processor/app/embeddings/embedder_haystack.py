import os
from typing import List
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.dataclasses import Document

# Podés cambiar el modelo si querés otro ST: all-mpnet-base-v2, etc.
MODEL_NAME = os.getenv("HAYSTACK_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Inicializamos una vez (warm-up)
_doc_embedder = SentenceTransformersDocumentEmbedder(model=MODEL_NAME)
_doc_embedder.warm_up()

def embed_texts_haystack(texts: List[str]) -> list[list[float]]:
    """
    Recibe lista de textos (chunks) y devuelve lista de vectores (uno por texto).
    """
    docs = [Document(content=t) for t in texts]
    res = _doc_embedder.run(documents=docs)
    out_docs = res["documents"]
    # Cada Document ahora trae .embedding (lista de floats)
    return [d.embedding for d in out_docs]
