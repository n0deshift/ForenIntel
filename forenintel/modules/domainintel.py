import os, json, requests, subprocess
from datetime import datetime

def whois(domain):
    try:
        out = subprocess.check_output(["whois", domain], timeout=10, text=True, errors="ignore")
        lines = [l for l in out.splitlines() if any(k in l.lower() for k in ["registrar", "creation", "expiry", "country"])]
        return lines[:10]
    except Exception:
        return []

def headers(domain):
    try:
        r = requests.get(f"https://{domain}", timeout=10)
        return dict(r.headers)
    except Exception:
        return {}

def run_domainintel(case_id, domain):
    outdir = os.path.join("cases", case_id, "intelligence")
    os.makedirs(outdir, exist_ok=True)

    data = {
        "module": "Domain Intelligence",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "input": {"domain": domain},
        "results": {
            "whois_summary": whois(domain),
            "http_headers": headers(domain)
        }
    }

    with open(os.path.join(outdir, "domain.json"), "w") as f:
        json.dump(data, f, indent=4)

    print("[+] Domain intelligence saved")

