from core.ban_controller import restore_bans, unban_expired
from scripts.task_manager import run_tasks
import time

def main():
    print("Netguard Service Started")

    restore_bans()

    while True:
        run_tasks()
        unban_expired()
        time.sleep(60)

if __name__ == "__main__":
    main()