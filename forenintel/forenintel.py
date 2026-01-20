#!/usr/bin/env python3

from forenintel.cli.parser import build_parser
from forenintel.utils.logger import setup_logger

def main():
    logger = setup_logger()
    parser = build_parser()
    args = parser.parse_args()

    logger.info(f"Command executed: {args}")

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
