import json
from pathlib import Path

DB_FILE = Path("/home/netguard/netguard/db/bans.json")

with open(DB_FILE, "r") as f:
    data = json.load(f)

print("Active Bans:")
for item in data["banned_ips"]:
    print(item["ip"])