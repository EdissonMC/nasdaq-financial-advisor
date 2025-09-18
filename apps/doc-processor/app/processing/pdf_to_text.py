import fitz, re
HEADER_FOOTER = re.compile(r'^\s*(Table of Contents|Contents|Page \d+ of \d+)\s*$', re.I)

def clean_page(text: str) -> str:
    lines = []
    for ln in text.splitlines():
        if not HEADER_FOOTER.match(ln.strip()):
            ln = ln.replace("\u00ad", "")  # soft hyphen
            lines.append(ln)
    return "\n".join(lines)

def extract_pages_text(pdf_path: str) -> list[dict]:
    out = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            txt = page.get_text("text") or ""
            out.append({"page": i+1, "text": clean_page(txt)})
    return out
