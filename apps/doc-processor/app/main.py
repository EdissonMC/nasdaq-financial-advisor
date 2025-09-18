import argparse, csv, json, time, uuid
from pathlib import Path
from app.processing.pdf_to_text import extract_pages_text
from app.processing.chunker import chunk_document
from app.eda.quick_eda import run_quick_eda
import random
import os, glob
from app.embeddings.embedder_haystack import embed_texts_haystack
from app.indexing.upsert_vectors import upsert_pinecone
from sentence_transformers import SentenceTransformer
from typing import List
import textwrap
import requests
from pinecone import Pinecone


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
idx = pc.Index(os.getenv("PINECONE_INDEX","financial-docs"))

CHUNKS_DIR = "/data/outputs/chunks"

def _iter_chunk_files():
    for p in glob.glob(os.path.join(CHUNKS_DIR, "*.jsonl")):
        yield p

def _estimate_batch_bytes(vecs, ids, metas):
    # vecs: List[List[float]]
    if not vecs:
        return 0
    dim = len(vecs[0])
    # 4 bytes por float32
    vec_bytes = len(vecs) * dim * 4
    # ids + metadatos (aprox serializados)
    id_bytes = sum(len(i) for i in ids)
    meta_bytes = sum(len(json.dumps(m)) for m in metas)
    # overhead fijo por vector (alineación, headers de request, etc.)
    overhead = 64 * len(vecs)
    return vec_bytes + id_bytes + meta_bytes + overhead


def _read_jsonl(path: str, limit: int | None = None):
    n = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
            n += 1
            if limit and n >= limit:
                break

def index_haystack(
    limit_files: int | None,
    limit_chunks_per_file: int | None,
    batch_size: int = 64,
    target_gb: float | None = None,
    seed: int = 42,
):
    files = list(_iter_chunk_files())
    random.Random(seed).shuffle(files)  # barajar archivos

    if limit_files:
        files = files[:limit_files]

    target_bytes = int(target_gb * (1024**3)) if target_gb else None
    total_vectors = 0
    total_bytes = 0

    for fp in files:
        # Leer y mezclar las líneas de ese archivo (si querés aleatoriedad intra-archivo)
        recs = list(_read_jsonl(fp, limit_chunks_per_file))
        random.shuffle(recs)

        texts, metas, ids = [], [], []
        local = 0

        for rec in recs:
            txt = rec["text"]
            md = rec["metadata"]
            vid = f'{md["document_id"]}:{md["chunk_index"]}'
            texts.append(txt); metas.append(md); ids.append(vid)

            if len(texts) >= batch_size:
                vecs = embed_texts_haystack(texts)
                items = [{"id": ids[i], "values": vecs[i], "metadata": metas[i]} for i in range(len(texts))]
                upsert_pinecone(items)
                local += len(items)
                total_vectors += len(items)
                batch_bytes = _estimate_batch_bytes(vecs, ids, metas)
                total_bytes += batch_bytes

                print(f"Upserted {len(items)} vectors from {os.path.basename(fp)} | +{batch_bytes/1_048_576:.2f} MiB | total ~{total_bytes/1_048_576:.2f} MiB")

                texts, metas, ids = [], [], []

                if target_bytes and total_bytes >= target_bytes:
                    print(f"TARGET REACHED ~{total_bytes/1_048_576:.2f} MiB ({total_vectors} vectors). Stopping.")
                    print(f"TOTAL upserts: {total_vectors}")
                    return

        if texts:
            vecs = embed_texts_haystack(texts)
            items = [{"id": ids[i], "values": vecs[i], "metadata": metas[i]} for i in range(len(texts))]
            upsert_pinecone(items)
            local += len(items)
            total_vectors += len(items)
            batch_bytes = _estimate_batch_bytes(vecs, ids, metas)
            total_bytes += batch_bytes
            print(f"Upserted {len(items)} vectors from {os.path.basename(fp)} | +{batch_bytes/1_048_576:.2f} MiB | total ~{total_bytes/1_048_576:.2f} MiB")

            if target_bytes and total_bytes >= target_bytes:
                print(f"TARGET REACHED ~{total_bytes/1_048_576:.2f} MiB ({total_vectors} vectors). Stopping.")
                print(f"TOTAL upserts: {total_vectors}")
                return

        print(f"Indexed {local} vectors from {os.path.basename(fp)}")

    print(f"TOTAL upserts: {total_vectors} (~{total_bytes/1_048_576:.2f} MiB)")

OUT_DIR = Path("/data/outputs/chunks")

def process_one(pdf_path: str, meta: dict):
    did = str(uuid.uuid4())
    meta_base = {
        "document_id": did,
        "company": meta.get("company"),
        "filing_year": int(meta["filing_year"]) if meta.get("filing_year") else None,
        "document_type": meta.get("document_type"),
        "source_path": pdf_path,
        "processed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    pages = extract_pages_text(pdf_path)
    chunks = list(chunk_document(pages, meta_base))
    out = OUT_DIR / f"{did}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for ch in chunks: f.write(json.dumps(ch, ensure_ascii=False)+"\n")
    return did, len(chunks), str(out)

def backfill(manifest_csv: str, limit: int | None, seed: int = 42):
    import random
    rows = []
    with open(manifest_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    random.Random(seed).shuffle(rows)
    if limit: 
        rows = rows[:limit]

    done = 0
    for row in rows:
        try:
            did, n, out = process_one(row["path"], row)
            print("OK", n, out)
        except Exception as e:
            print("FAIL", row["path"], e)
        done += 1

def _read_chunk_text_by_id(doc_id: str, chunk_index: int, base_dir: str = CHUNKS_DIR) -> str | None:
    fp = os.path.join(base_dir, f"{doc_id}.jsonl")
    if not os.path.exists(fp):
        return None
    with open(fp, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == int(chunk_index):
                rec = json.loads(line)
                return rec.get("text")
    return None

def search_query(query: str, top_k: int = 5):
    model_name = os.getenv("HAYSTACK_MODEL","sentence-transformers/all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)

    # 1) embed de la pregunta con el MISMO modelo
    qvec = model.encode([query], normalize_embeddings=True)[0].tolist()

    # 2) consulta a Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    idx = pc.Index(os.getenv("PINECONE_INDEX","financial-docs"))
    res = idx.query(vector=qvec, top_k=top_k, include_metadata=True)

    # 3) imprimir resultados lindos
    matches: List[dict] = res.get("matches", [])
    if not matches:
        print("Sin resultados.")
        return
    print(f"\nTop-{top_k} resultados para: {query}\n")
    for m in matches:
        md = m.get("metadata", {}) or {}
        did, cidx = m["id"].split(":")
        full_text = _read_chunk_text_by_id(did, int(cidx))  # ← acá recuperás el chunk completo

        comp = md.get("company"); year = md.get("filing_year")
        dtype = md.get("document_type"); p0, p1 = md.get("page_start"), md.get("page_end")
        preview = md.get("text_preview") or md.get("section") or ""

        print(f"score={m['score']:.3f} | {comp} {year} | {dtype} | p.{p0}-{p1} | id={m['id']}")
        if preview:
            print(f"  ▶ {preview[:180]}{'...' if len(preview)>180 else ''}")
        if full_text:
            # muestra un poco más del chunk verdadero (opcional)
            print(f"  🧩 {full_text[:400]}{'...' if len(full_text)>400 else ''}")

    print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("manifest")
    p1.add_argument("--root", required=True)
    p1.add_argument("--out", default="/data/manifest.csv")

    p2 = sub.add_parser("eda")
    p2.add_argument("--manifest", required=True)
    p2.add_argument("--limit", type=int, default=200)
    p2.add_argument("--out", default="/data/outputs/eda/eda_sample_stats.csv")

    p3 = sub.add_parser("backfill")
    p3.add_argument("--manifest", required=True)
    p3.add_argument("--limit", type=int)
    p3.add_argument("--seed", type=int, default=42)

    p4 = sub.add_parser("index")
    p4.add_argument("--limit-files", type=int)
    p4.add_argument("--limit-chunks-per-file", type=int)
    p4.add_argument("--batch-size", type=int, default=64)
    p4.add_argument("--target-gb", type=float)        # ej: 2.0
    p4.add_argument("--seed", type=int, default=42)   # reproducibilidad
    # parser
    p5 = sub.add_parser("search")
    p5.add_argument("--query", required=True)
    p5.add_argument("--top-k", type=int, default=5)

    args = ap.parse_args()

    if args.cmd == "manifest":
        from app.ingestion.manifest import build_local_manifest
        build_local_manifest(args.root, args.out)
    elif args.cmd == "eda":
        run_quick_eda(args.manifest, args.limit, args.out)
    elif args.cmd == "backfill":
        backfill(args.manifest, args.limit, args.seed)
    elif args.cmd == "index":
        index_haystack(args.limit_files, args.limit_chunks_per_file, args.batch_size, args.target_gb, args.seed)
    elif args.cmd == "search":
        search_query(args.query, args.top_k)


