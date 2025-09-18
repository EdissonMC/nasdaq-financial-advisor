import os
import json
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from typing import List

CHUNKS_DIR = "/data/outputs/chunks"

class PineconeSearcher:
    def __init__(self, 
                 api_key: str = None, 
                 index_name: str = None, 
                 model_name: str = None, 
                 chunks_dir: str = CHUNKS_DIR):
        
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.index_name = index_name or os.getenv("PINECONE_INDEX", "financial-docs")
        self.model_name = model_name or os.getenv("HAYSTACK_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.chunks_dir = chunks_dir
        self.pc = Pinecone(api_key=self.api_key)
        self.idx = self.pc.Index(self.index_name)
        self.model = SentenceTransformer(self.model_name)

    def _read_chunk_text_by_id(self, doc_id: str, chunk_index: int) -> str | None:
        fp = os.path.join(self.chunks_dir, f"{doc_id}.jsonl")
        if not os.path.exists(fp):
            return None
        with open(fp, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i == int(chunk_index):
                    rec = json.loads(line)
                    return rec.get("text")
        return None

    def search_query(self, query: str, top_k: int = 5):
        # 1) embed de la pregunta con el MISMO modelo
        qvec = self.model.encode([query], normalize_embeddings=True)[0].tolist()
        # 2) consulta a Pinecone
        res = self.idx.query(vector=qvec, top_k=top_k, include_metadata=True)
        # 3) imprimir resultados lindos
        matches: List[dict] = res.get("matches", [])
        if not matches:
            print("Sin resultados.")
            return
        print(f"\nTop-{top_k} resultados para: {query}\n")
        for m in matches:
            md = m.get("metadata", {}) or {}
            did, cidx = m["id"].split(":")
            full_text = self._read_chunk_text_by_id(did, int(cidx))
            comp = md.get("company"); year = md.get("filing_year")
            dtype = md.get("document_type"); p0, p1 = md.get("page_start"), md.get("page_end")
            preview = md.get("text_preview") or md.get("section") or ""
            print(f"score={m['score']:.3f} | {comp} {year} | {dtype} | p.{p0}-{p1} | id={m['id']}")
            if preview:
                print(f"  ▶ {preview[:180]}{'...' if len(preview)>180 else ''}")
            if full_text:
                print(f"  🧩 {full_text[:400]}{'...' if len(full_text)>400 else ''}")
        print()
        
        

if __name__ == "__main__":
    searcher = PineconeSearcher()
    searcher.search_query("Apple’s most valuable market", 5)