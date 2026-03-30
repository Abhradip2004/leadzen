from .session import fetch_all

def get_all_email_inboxes():
    stmt = "SELECT * FROM email_inboxes"
    return fetch_all(stmt)

