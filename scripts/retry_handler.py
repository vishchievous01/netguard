import time
from scripts.logger import get_logger

logger = get_logger()

def retry(task_function, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            return task_function()
        except Exception as e:
            logger.error(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                logger.critical("Task failed after maximum retries.")