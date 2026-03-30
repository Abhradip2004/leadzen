import imaplib
import email
from app.db.email_inboxes import get_all_email_inboxes
from app.services.whatsapp_service import process_internal_message


class EmailService:
    async def check_all_inboxes(self):
        inboxes = get_all_email_inboxes()

        for inbox in inboxes:
            try:
                mail = imaplib.IMAP4_SSL(inbox["imap_server"])
                mail.login(inbox["imap_user"], inbox["imap_password"])
                mail.select("inbox")

                status, messages = mail.search(None, "UNSEEN")

                for num in messages[0].split():
                    _, msg_data = mail.fetch(num, "(RFC822)")
                    msg = email.message_from_bytes(msg_data[0][1])

                    sender = msg.get("From", "")
                    subject = msg.get("Subject", "")
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    full_message = f"{subject}\n{body}"

                    await process_internal_message(
                        user_id=sender,
                        message=full_message,
                        channel="email",
                        organization_id=inbox["organization_id"],
                    )

                mail.logout()

            except Exception as e:
                print(f"Email processing error: {e}")