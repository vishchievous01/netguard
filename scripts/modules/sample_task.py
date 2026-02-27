import random
from scripts.logger import get_logger

logger = get_logger()

def run():
    logger.info("Running sample security task...")

    if random.choice([True, False]):
        raise Exception("Simulated failure")
    
    logger.info("Sample task completed successfully.")