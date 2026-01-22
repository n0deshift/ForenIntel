import os, json, requests
from datetime import datetime

HEADERS = {"User-Agent": "ForenIntel/1.0 (Academic OSINT)"}

def exists(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.status_code == 200
    except requests.RequestException:
        return False

def run_social(case_id, username):
    outdir = os.path.join("cases", case_id, "intelligence")
    os.makedirs(outdir, exist_ok=True)

    results = [
        {"platform": "X", "url": f"https://x.com/{username}", "exists": exists(f"https://x.com/{username}")},
        {"platform": "Instagram", "url": f"https://www.instagram.com/{username}", "exists": exists(f"https://www.instagram.com/{username}")},
        {"platform": "Medium", "url": f"https://medium.com/@{username}", "exists": exists(f"https://medium.com/@{username}")},
    ]

    data = {
        "module": "Social Footprint",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "input": {"username": username},
        "results": results
    }

    with open(os.path.join(outdir, "social.json"), "w") as f:
        json.dump(data, f, indent=4)

    print("[+] Social footprint saved")
