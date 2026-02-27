from scripts.logger import get_logger
from scripts.alert_engine import send_alert
from db.ban_manager import ban_ip

logger = get_logger()

AUTH_LOG = "/var/log/auth.log"

MAX_ATTEMPTS = 5
TIME_WINDOW = 10


def run():
    logger.info("Starting SSH brute-force detection...")

    from datetime import datetime, timedelta, timezone
    import re
    from collections import defaultdict

    failed_attempts = defaultdict(list)

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=TIME_WINDOW)

    try:
        with open(AUTH_LOG, "r", errors="ignore") as f:
            lines = f.readlines()[-500:]
    except Exception as e:
        logger.error(f"Error reading auth log: {e}")
        return

    for line in lines:

        match = re.search(
            r"Failed password.*from (\d+\.\d+\.\d+\.\d+)",
            line
        )

        if not match:
            continue

        ip = match.group(1)

        try:
            ts = line.split()[0]
            timestamp = datetime.fromisoformat(ts)
        except Exception:
            continue

        if timestamp >= window_start:
            failed_attempts[ip].append(timestamp)

        repeat_match = re.search(r"message repeated (\d+) times", line)
        if repeat_match:
            repeat_count = int(repeat_match.group(1))
            for _ in range(repeat_count):
                failed_attempts[ip].append(timestamp)

    for ip, attempts in failed_attempts.items():

        logger.info(f"{ip} -> {len(attempts)} failed attempts")

        if len(attempts) >= MAX_ATTEMPTS:

            logger.warning(
                f"Blocking IP {ip} after {len(attempts)} failed attempts"
            )

            msg = (
                f"SSH brute-force Detected\n"
                f"IP Address: {ip}\n"
                f"Failed Attempts: {len(attempts)}\n"
                f"Time Window: {TIME_WINDOW} minutes"
            )

            send_alert("SSH Brute-force Alert Detected", msg)

            ban_ip(ip)

    logger.info("SSH brute-force detection completed.")