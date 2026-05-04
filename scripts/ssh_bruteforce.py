import re
import json
from collections import defaultdict

LOG_FILE = "/var/log/auth.log"
BAN_FILE = "bans.json"
THRESHOLD = 5

failed_attempts = defaultdict(int)

# Regex to extract IP
pattern = re.compile(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)")

def load_existing_bans():
    try:
        with open(BAN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_bans(banned_ips):
    with open(BAN_FILE, "w") as f:
        json.dump(list(banned_ips), f, indent=4)

def detect():
    existing_bans = load_existing_bans()

    with open(LOG_FILE, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                ip = match.group(1)
                failed_attempts[ip] += 1

    new_bans = set()

    for ip, count in failed_attempts.items():
        if count >= THRESHOLD and ip not in existing_bans:
            print(f"[!] Detected brute force from {ip} ({count} attempts)")
            new_bans.add(ip)

    updated_bans = existing_bans.union(new_bans)
    save_bans(updated_bans)

if __name__ == "__main__":
    detect()