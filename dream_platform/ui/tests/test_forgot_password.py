import time

from playwright.sync_api import expect
from dream_platform.conftest import get_last_reset_email_graph
from dream_platform.ui.pages.login_page import LoginPage
from dream_platform.ui.pages.forgot_password_page import ForgotPasswordPage
from dream_platform.ui.pages.reset_password_page import ResetPasswordPage
from dream_platform.utils.helper import restore_password, extract_reset_link

# -------- Check Forgot Password page elements ----------
def test_forgot_password_page_elements(browser_page, base_url):
    login = LoginPage(browser_page, base_url)
    login.open_login()
    login.click_forgot_password()

    forgot = ForgotPasswordPage(browser_page, base_url)
    expect(browser_page).to_have_url(f"{base_url}password-reset")
    expect(forgot.header).to_be_visible()
    expect(forgot.description).to_be_visible()
    expect(forgot.email_input).to_be_visible()
    expect(forgot.restore_button).to_be_disabled()
    time.sleep(1)

# --------- Send reset email and verify success message ----------
def test_forgot_password_send_email_ui(browser_page, base_url, config):
    forgot = ForgotPasswordPage(browser_page, base_url)
    forgot.restore_password(config["users"]["user"]["username"])
    time.sleep(1)
    expect(forgot.success_message).to_be_visible()

 # Full flow: read email, open reset link, reset password ----------
def test_forgot_password_full_flow(browser_page, base_url, config):
    """One full orchestrated test: send email → fetch → reset → verify → restore"""
    creds = config["users"]["user"]

    # Step 1: Wait for email and extract link
    email_content = get_last_reset_email_graph(creds["username"])
    reset_link = extract_reset_link(email_content)

    # Step 2: Reset password
    browser_page.goto(reset_link)
    reset = ResetPasswordPage(browser_page)
    time.sleep(1)

    reset.enter_new_password(creds["new_pass"])
    reset.click_save()

    # Step 3: Verify login works
    login = LoginPage(browser_page, base_url)
    login.open_login()
    login.enter_username(creds["username"])
    login.enter_password(creds["new_pass"])
    login.click_login()

    expect(login.user_profile_link).to_be_visible()

    #logout
    time.sleep(1)
    login.click_logout()
    login.confirm_logout()
    # Step 4: Restore original password
    restore_password(browser_page, base_url, config)