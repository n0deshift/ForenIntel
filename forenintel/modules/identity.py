import os
import json
import requests
from datetime import datetime

HEADERS = {
    "User-Agent": "ForenIntel/1.0 (Academic Digital Forensics Research)"
}

def profile_exists(url):
    """
    Checks whether a public profile exists by HTTP status code.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def run_identity(case_id, username, email=None):
    """
    Perform Identity Intelligence (Username / Email footprint).
    Results are stored inside the case intelligence directory.
    """

    case_base = os.path.join("cases", case_id)
    intel_dir = os.path.join(case_base, "intelligence")
    os.makedirs(intel_dir, exist_ok=True)

    findings = {
        "module": "Identity Intelligence",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "input": {
            "username": username,
            "email": email
        },
        "results": [],
        "confidence_score": 0
    }

    score = 0

    # -------- GitHub --------
    github_url = f"https://github.com/{username}"
    github_found = profile_exists(github_url)
    findings["results"].append({
        "platform": "GitHub",
        "url": github_url,
        "profile_exists": github_found
    })
    if github_found:
        score += 1

    # -------- Reddit --------
    reddit_url = f"https://www.reddit.com/user/{username}"
    reddit_found = profile_exists(reddit_url)
    findings["results"].append({
        "platform": "Reddit",
        "url": reddit_url,
        "profile_exists": reddit_found
    })
    if reddit_found:
        score += 1

    # -------- Email Indicator (No Breach APIs) --------
    if email:
        findings["results"].append({
            "platform": "Email Provided",
            "indicator": "Email supplied by investigator (no breach lookup performed)"
        })
        score += 1

    findings["confidence_score"] = score

    output_file = os.path.join(intel_dir, "identity.json")
    with open(output_file, "w") as f:
        json.dump(findings, f, indent=4)

    print(f"[+] Identity intelligence saved to {output_file}")
