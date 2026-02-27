import os
import smtplib
import requests
from email.message import EmailMessage
from dotenv import load_dotenv

from scripts.logger import get_logger


load_dotenv("/home/netguard/netguard/.env")

logger = get_logger()

TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT = os.getenv("TELEGRAM_CHAT_ID")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")


def send_telegram(message):

    if not TG_TOKEN or not TG_CHAT:
        logger.warning("Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"

    data = {
        "chat_id": TG_CHAT,
        "text": message
    }

    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        logger.error(f"Telegram error: {e}")


def send_email(subject, body):

    if not EMAIL_USER or not EMAIL_PASS:
        logger.warning("Email not configured")
        return

    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = ALERT_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

    except Exception as e:
        logger.error(f"Email error: {e}")


def send_alert(title, message):

    full_message = f"[NetGuard ALERT]\n{title}\n\n{message}"

    send_telegram(full_message)
    send_email(title, full_message)

    logger.warning("Alert sent successfully")