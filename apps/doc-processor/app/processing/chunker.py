from typing import Iterable
import tiktoken
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def token_len(enc, s: str) -> int:
    return len(enc.encode(s))

def chunk_document(pages: list[dict], meta_base: dict) -> Iterable[dict]:
    enc = tiktoken.get_encoding("cl100k_base")
    buf, buf_tokens, idx = [], 0, 0
    page_start = None

    def flush(page_end):
        nonlocal buf, buf_tokens, idx, page_start
        text = "\n".join(buf).strip()
        if not text: return None
        md = dict(meta_base)
        md.update({
            "page_start": page_start,
            "page_end": page_end,
            "chunk_index": idx,
            "chunk_size_tokens": token_len(enc, text),
        })
        idx += 1
        return {"text": text, "metadata": md}

    chunks = []
    for p in pages:
        if page_start is None: page_start = p["page"]
        for ln in p["text"].splitlines():
            ln_tokens = token_len(enc, ln+"\n")
            if buf_tokens + ln_tokens > CHUNK_SIZE:
                c = flush(p["page"])
                if c: chunks.append(c)
                # overlap: conserva últimas líneas hasta CHUNK_OVERLAP
                back, bt = [], 0
                for l in reversed(buf[-60:]):
                    t = token_len(enc, l+"\n")
                    if bt + t > CHUNK_OVERLAP: break
                    back.append(l); bt += t
                buf = list(reversed(back)); buf_tokens = bt; page_start = p["page"]
            buf.append(ln); buf_tokens += ln_tokens

    if buf:
        c = flush(pages[-1]["page"])
        if c: chunks.append(c)
    return chunks
