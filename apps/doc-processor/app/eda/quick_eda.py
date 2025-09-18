import csv, random, statistics, re
import fitz

def is_light(txt: str, min_chars=40) -> bool:
    import re
    return len(re.sub(r'\s+','',txt)) < min_chars

def pdf_stats(path: str) -> dict:
    with fitz.open(path) as doc:
        lens, light = [], 0
        for pg in doc:
            t = pg.get_text("text") or ""
            lens.append(len(t))
            light += int(is_light(t))
    return {
        "path": path,
        "pages": len(lens),
        "chars_total": sum(lens),
        "chars_median": int(statistics.median(lens) if lens else 0),
        "light_ratio": round(light/max(1,len(lens)), 3),
    }

def run_quick_eda(manifest_csv: str, sample_size: int, out_csv: str):
    paths = []
    with open(manifest_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["source"] == "local": paths.append(r["path"])
    sample = random.sample(paths, k=min(sample_size, len(paths)))
    rows = []
    for p in sample:
        try: rows.append(pdf_stats(p))
        except Exception as e: rows.append({"path": p, "error": str(e)})
    import os
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    fields = sorted({k for d in rows for k in d.keys()})
    with open(out_csv,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for d in rows: w.writerow(d)
    print(f"EDA listo → {out_csv}")
