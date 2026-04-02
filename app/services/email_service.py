import imaplib
import email
from email.header import decode_header

from app.db.email_inboxes import get_all_email_inboxes
from app.services.whatsapp_service import process_internal_message


class EmailService:
    """
    Handles ingestion of emails via IMAP and forwards them
    into the internal message processing pipeline.
    """

    def _connect(self, imap_server: str, username: str, password: str):
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        return mail

    def _decode_header(self, value: str) -> str:
        if not value:
            return ""

        decoded_parts = decode_header(value)
        decoded_string = ""

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_string += part.decode(encoding or "utf-8", errors="ignore")
            else:
                decoded_string += part

        return decoded_string

    def _extract_body(self, msg) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition", ""))

                if content_type == "text/plain" and "attachment" not in disposition:
                    return part.get_payload(decode=True).decode(errors="ignore")
        else:
            return msg.get_payload(decode=True).decode(errors="ignore")

        return ""

    def _extract_sender(self, raw_sender: str) -> str:
        if "<" in raw_sender and ">" in raw_sender:
            return raw_sender.split("<")[1].split(">")[0]
        return raw_sender.strip()

    async def check_all_inboxes(self):
        inboxes = get_all_email_inboxes()

        for inbox in inboxes:
            mail = None

            try:
                mail = self._connect(
                    inbox["imap_server"],
                    inbox["imap_user"],
                    inbox["imap_password"],
                )

                mail.select("inbox")

                status, messages = mail.search(None, "UNSEEN")
                if status != "OK":
                    continue

                for num in messages[0].split():
                    _, msg_data = mail.fetch(num, "(RFC822)")

                    if not msg_data or not msg_data[0]:
                        continue

                    msg = email.message_from_bytes(msg_data[0][1])

                    sender = self._extract_sender(msg.get("From", ""))
                    subject = self._decode_header(msg.get("Subject", ""))
                    body = self._extract_body(msg)
                    message_id = msg.get("Message-ID", "")

                    full_message = f"{subject}\n{body}".strip()

                    if not sender or not full_message:
                        continue

                    await process_internal_message(
                        user_id=sender,
                        message=full_message,
                        channel="email",
                        organization_id=inbox["organization_id"],
                        metadata={
                            "subject": subject,
                            "message_id": message_id,
                        },
                    )

            except Exception as e:
                print(f"[EmailService] Error processing inbox {inbox.get('email_address')}: {e}")

            finally:
                try:
                    if mail:
                        mail.logout()
                except Exception:
                    pass