import re
from collections import defaultdict
from security.ban_controller import ban_ip

LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5
CHECK_LINES = 200

def run():
    print("Starting SSH brute-force detection...")

    ip_counter = defaultdict(int)

    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-CHECK_LINES:]

    except FileNotFoundError:
        print("auth.log not found.")
        return

    for line in lines:
        if "Failed password" in line:
            match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip = match.group(1)
                ip_counter[ip] += 1

    for ip, count in ip_counter.items():
        if count >= THRESHOLD:
            print(f"Banning {ip} after {count} failed attempts")
            ban_ip(ip)

    print("SSH brute-force detection completed.")