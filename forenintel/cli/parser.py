import argparse
import os

from forenintel.case.manager import create_case, load_case
from forenintel.modules.identity import run_identity
from forenintel.modules.infrastructure import run_infrastructure
from forenintel.modules.social import run_social
from forenintel.modules.domainintel import run_domainintel
from forenintel.modules.pasteintel import run_pasteintel


def build_parser():
    parser = argparse.ArgumentParser(
        prog="forenintel",
        description="ForenIntel - Digital Forensic Intelligence Framework"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ---------------- CASE COMMAND ----------------
    case_parser = subparsers.add_parser("case", help="Case management")
    case_sub = case_parser.add_subparsers(dest="action")

    case_create = case_sub.add_parser("create", help="Create a new case")
    case_create.add_argument("case_id")
    case_create.set_defaults(func=lambda a: create_case(a.case_id))

    case_load = case_sub.add_parser("load", help="Load an existing case")
    case_load.add_argument("case_id")
    case_load.set_defaults(func=lambda a: load_case(a.case_id))

    # ---------------- COLLECT COMMAND ----------------
    collect_parser = subparsers.add_parser("collect", help="Collect intelligence")
    collect_sub = collect_parser.add_subparsers(dest="type")

    # Identity
    identity = collect_sub.add_parser("identity", help="Identity intelligence")
    identity.add_argument("--username", required=True)
    identity.add_argument("--email", required=False)
    identity.set_defaults(func=handle_identity)

    # Infrastructure
    infrastructure = collect_sub.add_parser("infrastructure", help="Infrastructure intelligence")
    infrastructure.add_argument("--domain", required=True)
    infrastructure.add_argument("--ip", required=False)
    infrastructure.set_defaults(func=handle_infrastructure)

    # Social footprint
    social = collect_sub.add_parser("social", help="Social footprint")
    social.add_argument("--username", required=True)
    social.set_defaults(func=handle_social)

    # Domain intelligence
    domain = collect_sub.add_parser("domain", help="Domain intelligence")
    domain.add_argument("--domain", required=True)
    domain.set_defaults(func=handle_domain)

    # Paste intelligence
    paste = collect_sub.add_parser("paste", help="Paste / leak indicators")
    paste.add_argument("--keyword", required=True)
    paste.set_defaults(func=handle_paste)

    return parser


def get_active_case():
    if not os.path.exists(".active_case"):
        print("[!] No active case loaded. Use: case load <case_id>")
        return None
    with open(".active_case", "r") as f:
        return f.read().strip()


def handle_identity(args):
    case_id = get_active_case()
    if not case_id:
        return
    run_identity(case_id, args.username, args.email)


def handle_infrastructure(args):
    case_id = get_active_case()
    if not case_id:
        return
    run_infrastructure(case_id, args.domain, args.ip)


def handle_social(args):
    case_id = get_active_case()
    if not case_id:
        return
    run_social(case_id, args.username)


def handle_domain(args):
    case_id = get_active_case()
    if not case_id:
        return
    run_domainintel(case_id, args.domain)


def handle_paste(args):
    case_id = get_active_case()
    if not case_id:
        return
    run_pasteintel(case_id, args.keyword)
