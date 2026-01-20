import os
import json
from datetime import datetime

BASE_CASE_DIR = "cases"
ACTIVE_CASE_FILE = ".active_case"

def create_case(case_id):
    case_path = os.path.join(BASE_CASE_DIR, case_id)

    if os.path.exists(case_path):
        print(f"[!] Case '{case_id}' already exists")
        return

    os.makedirs(case_path)
    os.makedirs(os.path.join(case_path, "evidence"))
    os.makedirs(os.path.join(case_path, "intelligence"))
    os.makedirs(os.path.join(case_path, "analysis"))
    os.makedirs(os.path.join(case_path, "reports"))
    os.makedirs(os.path.join(case_path, "logs"))

    metadata = {
        "case_id": case_id,
        "created_at": datetime.utcnow().isoformat(),
        "status": "active"
    }

    with open(os.path.join(case_path, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"[+] Case '{case_id}' created successfully")

def load_case(case_id):
    case_path = os.path.join(BASE_CASE_DIR, case_id)

    if not os.path.exists(case_path):
        print(f"[!] Case '{case_id}' does not exist")
        return

    with open(ACTIVE_CASE_FILE, "w") as f:
        f.write(case_id)

    print(f"[+] Case '{case_id}' loaded as active case")
