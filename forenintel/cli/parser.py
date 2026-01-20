import argparse
from forenintel.case.manager import create_case, load_case

def build_parser():
    parser = argparse.ArgumentParser(
        prog="forenintel",
        description="ForenIntel - Digital Forensic Intelligence Framework"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ---- CASE COMMAND ----
    case_parser = subparsers.add_parser("case", help="Case management")
    case_sub = case_parser.add_subparsers(dest="action")

    case_create = case_sub.add_parser("create", help="Create a new case")
    case_create.add_argument("case_id")
    case_create.set_defaults(func=handle_case_create)

    case_load = case_sub.add_parser("load", help="Load an existing case")
    case_load.add_argument("case_id")
    case_load.set_defaults(func=handle_case_load)

    return parser

def handle_case_create(args):
    create_case(args.case_id)

def handle_case_load(args):
    load_case(args.case_id)
