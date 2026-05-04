import os
import sys
import django
import logging
from collections import defaultdict
import geoip2.database

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

sys.path.append(PROJECT_ROOT)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend.backend.settings"
)

django.setup()

LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "ssh_monitor.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)


# -----------------------------
# Imports after Django setup
# -----------------------------
from security.ban_controller import ban_ip
from reports.models import AttackEvent


# -----------------------------
# GeoIP Database
# -----------------------------
reader = geoip2.database.Reader("/usr/share/GeoIP/GeoLite2-City.mmdb")


LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5
CHECK_LINES = 200


# -----------------------------
# Extract attacker IP
# -----------------------------
def extract_ip(line):
    match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
    if match:
        return match.group(1)
    return None


# -----------------------------
# Extract username
# -----------------------------
def extract_username(line):
    match = re.search(r"for (\w+) from", line)
    if match:
        return match.group(1)
    return None


# -----------------------------
# GeoIP lookup
# -----------------------------
def get_geo(ip):

    country = None
    city = None
    lat = None
    lon = None

    try:
        response = reader.city(ip)

        country = response.country.name
        city = response.city.name
        lat = response.location.latitude
        lon = response.location.longitude

    except Exception:
        pass

    return country, city, lat, lon


# -----------------------------
# Main detection logic
# -----------------------------
def run():

    logging.info("Starting SSH brute-force detection")

    ip_counter = defaultdict(int)
    ip_usernames = {}

    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-CHECK_LINES:]

    except FileNotFoundError:
        logging.error("auth.log not found")
        return

    for line in lines:

        if (
            "Failed password" in line
            or "Invalid user" in line
            or "authentication failure" in line
        ):

            ip = extract_ip(line)
            username = extract_username(line)

            if ip:

                ip_counter[ip] += 1

                if username:
                    ip_usernames[ip] = username

    for ip, count in ip_counter.items():

        if count >= THRESHOLD:

            logging.warning(f"SSH brute force detected from {ip} ({count} attempts)")

            username = ip_usernames.get(ip)

            # Firewall block
            try:
                ban_ip(ip)
                logging.warning(f"IP blocked via iptables: {ip}")

            except Exception as e:
                logging.error(f"Firewall block failed for {ip}: {e}")

            # Geo lookup
            country, city, lat, lon = get_geo(ip)

            # Store event in database
            try:

                recent = (
                    AttackEvent.objects
                    .filter(
                        ip_address=ip,
                        event_type="SSH_BRUTE_FORCE"
                    )
                    .order_by("-timestamp")
                    .first()
                )

                if not recent or recent.attempts < count:

                    AttackEvent.objects.create(
                        ip_address=ip,
                        event_type="SSH_BRUTE_FORCE",
                        username=username,
                        country=country,
                        city=city,
                        latitude=lat,
                        longitude=lon,
                        attempts=count,
                        blocked=True
                    )

                    logging.info(f"Attack stored in DB: {ip} {country} {city}")

            except Exception as e:
                logging.error(f"Database logging failed: {e}")

    logging.info("SSH brute-force detection completed")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    run()