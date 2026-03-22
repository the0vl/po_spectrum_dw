import logging
import sys
from datetime import datetime

def get_logger(name):
    """Returns a pre-configured logger with timestamp and level."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. Output to Terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. Output to File (optional but recommended for DE)
    file_handler = logging.FileHandler('pipeline.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger