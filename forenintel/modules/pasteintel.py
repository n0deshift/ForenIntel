import os, json
from datetime import datetime
from duckduckgo_search import DDGS

def run_pasteintel(case_id, keyword):
    outdir = os.path.join("cases", case_id, "intelligence")
    os.makedirs(outdir, exist_ok=True)

    hits = []
    with DDGS() as ddgs:
        for r in ddgs.text(f'"{keyword}" leak paste', max_results=5):
            hits.append({"title": r.get("title"), "url": r.get("href")})

    data = {
        "module": "Paste & Leak Indicator",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "input": {"keyword": keyword},
        "results": hits
    }

    with open(os.path.join(outdir, "paste.json"), "w") as f:
        json.dump(data, f, indent=4)

    print("[+] Paste/leak indicators saved")
