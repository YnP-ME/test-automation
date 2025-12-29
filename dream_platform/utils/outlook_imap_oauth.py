import time
import email
from dream_platform.utils.helper import login_outlook_imap_app_only

def get_last_reset_email(username: str, max_wait=120):
    """
    Connects to Outlook via IMAP (OAuth) and fetches the latest password reset email body.
    """
    mail = login_outlook_imap_app_only(username)
    start_time = time.time()
    mail.select("inbox")

    while time.time() - start_time < max_wait:
        # Search for emails from your app's sender
        status, messages = mail.search(None, '(FROM "inquiries@quantumone.ae")')
        if status != "OK":
            time.sleep(5)
            continue

        msg_ids = messages[0].split()
        for msg_id in reversed(msg_ids):  # latest first
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            msg_date = email.utils.parsedate_to_datetime(msg["Date"])

            if msg_date.timestamp() < start_time:
                continue  # skip old emails

            # Get the email body (handle plain text and HTML)
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/html":
                        body = part.get_payload(decode=True).decode()
                        return body
            else:
                body = msg.get_payload(decode=True).decode()
                return body

        time.sleep(5)

    raise AssertionError("No new password reset email received")
