import logging
from datetime import datetime
import os

def setup_logger():
    logger = logging.getLogger("ForenIntel")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        handler = logging.FileHandler(
            os.path.join(log_dir, f"forenintel_{datetime.now().date()}.log")
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
