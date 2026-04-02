import os
import smtplib
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")


def send_email(
    to_email: str,
    message: str,
    subject: str = "Your inquiry",
    message_id: str = None,
):
    """
    Sends an email reply with proper threading support.
    """

    if not EMAIL or not PASSWORD:
        print("[EmailSender] Missing credentials")
        return

    msg = MIMEText(message)

    msg["Subject"] = f"Re: {subject}"
    msg["From"] = EMAIL
    msg["To"] = to_email

    if message_id:
        msg["In-Reply-To"] = message_id
        msg["References"] = message_id

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print(f"[EmailSender] Sent to {to_email}")

    except Exception as e:
        print(f"[EmailSender] Failed to send to {to_email}: {e}")