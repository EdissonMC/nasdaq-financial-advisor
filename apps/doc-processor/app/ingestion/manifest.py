from dataclasses import dataclass, asdict
from pathlib import Path
import csv, os, re

@dataclass
class DocEntry:
    source: str
    path: str
    filename: str
    company: str | None
    filing_year: int | None
    document_type: str | None

def guess_metadata_from_key(key: str):
    base = os.path.basename(key)
    m_year = re.search(r'(19|20)\d{2}', base)
    year = int(m_year.group(0)) if m_year else None
    m_type = re.search(r'(10-K|10-Q|20-F|6-K|8-K)', base, re.I)
    doctype = m_type.group(0).upper() if m_type else None
    company = Path(key).parent.name or None
    return company, year, doctype

def build_local_manifest(root_dir: str, out_csv: str):
    rows: list[DocEntry] = []
    for p in Path(root_dir).rglob("*.pdf"):
        if p.name == ".DS_Store": continue
        company, year, doctype = guess_metadata_from_key(str(p))
        rows.append(DocEntry("local", str(p), p.name, company, year, doctype))

    hdr = ["source","path","filename","company","filing_year","document_type"]
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr)
        w.writeheader()
        for r in rows: w.writerow(asdict(r))
    print(f"Manifest listo → {out_csv} ({len(rows)} archivos)")
