from loguru import logger
import os

LOG_DIR = os.path.expanduser("~/netguard/logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger.add(
    f"{LOG_DIR}/netguard.log",
    rotation="5 MB",
    retention="10 days",
    level="INFO",
    format="{time} | {level} | {message}",
)

def get_logger():
    return logger