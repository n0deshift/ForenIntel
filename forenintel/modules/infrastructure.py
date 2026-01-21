import os
import json
import socket
import requests
from datetime import datetime

HEADERS = {
    "User-Agent": "ForenIntel/1.0 (Academic Digital Forensics Research)"
}

def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def ssl_check(domain):
    try:
        sock = socket.create_connection((domain, 443), timeout=5)
        sock.close()
        return True
    except Exception:
        return False

def ip_geo(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass
    return {}

def run_infrastructure(case_id, domain, ip=None):
    base = os.path.join("cases", case_id)
    intel_dir = os.path.join(base, "intelligence")
    os.makedirs(intel_dir, exist_ok=True)

    result = {
        "module": "Infrastructure Intelligence",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "input": {
            "domain": domain,
            "ip": ip
        },
        "results": {}
    }

    resolved_ip = resolve_domain(domain)
    result["results"]["dns"] = {
        "resolved_ip": resolved_ip
    }

    result["results"]["ssl"] = {
        "https_open": ssl_check(domain)
    }

    geo_ip = ip or resolved_ip
    if geo_ip:
        result["results"]["ip_geolocation"] = ip_geo(geo_ip)
    else:
        result["results"]["ip_geolocation"] = {}

    out = os.path.join(intel_dir, "infrastructure.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[+] Infrastructure intelligence saved to {out}")
