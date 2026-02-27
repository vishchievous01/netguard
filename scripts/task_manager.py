from scripts.logger import get_logger
from scripts.retry_handler import retry
from scripts.modules import sample_task, ssh_monitor

logger = get_logger()

def run_tasks():
    tasks = [
        sample_task.run,
        ssh_monitor.run,
    ]

    for task in tasks:
        try:
            retry(task)
            logger.info(f"{task.__name__} executed successfully.")
        except Exception as e:
            logger.error(f"{task.__name__} failed permanently: {e}")