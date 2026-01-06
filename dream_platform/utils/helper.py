import time
from playwright.sync_api import expect
from dream_platform.ui.pages.login_page import LoginPage
from dream_platform.ui.pages.user_page import UserPage
import re
import imaplib
import base64
import msal
import os
from dotenv import load_dotenv

load_dotenv()

EMPLOYEE_USERNAME = os.getenv("EMPLOYEE_USERNAME")
EMPLOYEE_PASSWORD = os.getenv("EMPLOYEE_PASSWORD")
EMPLOYEE_NEW_PASSWORD = os.getenv("EMPLOYEE_NEW_PASSWORD")

IMAP_SERVER = "outlook.office365.com"
IMAP_PORT = 993
SCOPES = ["https://outlook.office365.com/.default"]
def restore_password(page, base_url):
    login = LoginPage(page, base_url)
    user = UserPage(page, base_url)

    login.open_login()
    login.enter_username(EMPLOYEE_USERNAME)
    login.enter_password(EMPLOYEE_NEW_PASSWORD)
    login.click_login()
    time.sleep(1)
    if user.user_profile_link.is_visible():
        user.click_user_icon()
        user.click_change_password()
        user.current_password_input.fill(EMPLOYEE_NEW_PASSWORD)
        user.new_password_input.fill(EMPLOYEE_PASSWORD)
        user.save_password_button.click()
        expect(user.password_change_success).to_be_visible()
        print("pass changed  successfully")

        login.click_logout()
        login.confirm_logout()

def extract_reset_link(email_content: str) -> str:
    links = re.findall(
        r"https?://dp\.dev\.qone-dev\.com/password-reset\?token=[A-Za-z0-9_\-]+",
        email_content
    )
    if not links:
        raise ValueError("No reset link found in email")
    return links[-1].strip().strip('"').strip("'")


def login_outlook_imap_app_only(username: str):
    """
    Logs into Outlook IMAP using app-only OAuth and returns an IMAP4_SSL object.
    """
    client_id = os.environ["AZURE_CLIENT_ID"]
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}"
    )

    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise Exception(f"Failed to get access token: {result}")

    access_token = result["access_token"]

    auth_string = base64.b64encode(
        f"user={username}\x01auth=Bearer {access_token}\x01\x01".encode()
    ).decode()

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.authenticate("XOAUTH2", lambda x: auth_string)
    return mail
