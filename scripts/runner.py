from scripts.task_manager import run_tasks
from db.ban_manager import restore_bans

def main():
    restore_bans()
    run_tasks()

if __name__ == "__main__":
    main()