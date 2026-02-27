from scripts.task_manager import run_tasks
from scripts.logger import get_logger

logger = get_logger()

def main():
    logger.info("Netguard Cron Runner Started")
    run_tasks()
    logger.info("Netguard Cron Runner Finished")

if __name__ == "__main__":
    main()