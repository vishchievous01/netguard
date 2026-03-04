import os
import django
import re
from collections import defaultdict

# Initialize Django so this script can use Django models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from security.ban_controller import ban_ip
from reports.models import AttackEvent


LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5
CHECK_LINES = 200


def extract_ip(line):
    """
    Extract attacker IP from SSH log line.
    """
    match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
    if match:
        return match.group(1)
    return None


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

        if (
            "Failed password" in line
            or "Invalid user" in line
            or "authentication failure" in line
        ):

            ip = extract_ip(line)

            if ip:
                ip_counter[ip] += 1

    for ip, count in ip_counter.items():

        if count >= THRESHOLD:

            print(f"Banning {ip} after {count} failed attempts")

            try:
                ban_ip(ip)
            except Exception as e:
                print(f"Firewall block failed: {e}")

            try:
                AttackEvent.objects.create(
                    ip_address=ip,
                    event_type="SSH_BRUTE_FORCE",
                    attempts=count,
                    blocked=True
                )
            except Exception as e:
                print(f"Database logging failed: {e}")

    print("SSH brute-force detection completed.")