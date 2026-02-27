import subprocess
from scripts.logger import get_logger

logger = get_logger()

def block_ip(ip):
    cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"
    ]

    try:
        subprocess.run(cmd, check=True)
        logger.warning(f"Blocked IP: {ip}")

    except Exception as e:
        logger.error(f"Failed to block IP {ip}: {e}")