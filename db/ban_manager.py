import json
import subprocess
import time
from pathlib import Path
from db.ban_manager import restore_bans
restore_bans()

DB_FILE = Path("/home/netguard/netguard/db/bans.json")

BAN_TIME = 1800


def load_db():
    if not DB_FILE.exists():
        return {
            "banned_ips": [],
            "whitelisted_ips": []
        }

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def ban_ip(ip):
    data = load_db()

    if ip in data["whitelisted_ips"]:
        return

    now = int(time.time())

    for item in data["banned_ips"]:
        if item["ip"] == ip:
            return

    subprocess.run(
        ["sudo", "iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"],
        check=False
    )

    data["banned_ips"].append({
        "ip": ip,
        "banned_at": now
    })

    save_db(data)


def unban_ip():
    data = load_db()
    now = int(time.time())

    active = []

    for item in data["banned_ips"]:

        # Still within ban time → keep
        if now - item["banned_at"] <= BAN_TIME:
            active.append(item)

        else:
            subprocess.run(
                ["sudo", "iptables", "-D", "INPUT", "-s", item["ip"], "-j", "DROP"],
                check=False
            )

    data["banned_ips"] = active
    save_db(data)

def restore_bans():
    data = load_db()

    for item in data["banned_ips"]:
        subprocess.run(
            ["sudo", "iptables", "-C", "INPUT", "-s", item["ip"], "-j", "DROP"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # If rule doesn't exist, add it
        subprocess.run(
            ["sudo", "iptables", "-I", "INPUT", "-s", item["ip"], "-j", "DROP"],
            check=False
        )