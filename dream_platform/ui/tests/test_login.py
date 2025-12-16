import time

from playwright.sync_api import expect
from dream_platform.ui.pages.login_page import LoginPage
import pytest

@pytest.mark.order(1)
def test_login_page_elements_before_login(page, base_url):
    login = LoginPage(page,base_url)
    login.open_login()

    time.sleep(2)

    expect(login.login_page_title, "Login page title is not visible").to_be_visible()
    expect(login.login_header_logo, "Company name is not visible on login page").to_be_visible()
    expect(login.username_input, "Username input is not visible").to_be_visible()
    expect(login.password_input, "Password input is not visible").to_be_visible()
    expect(login.login_button, "Login button is not visible").to_be_visible()

# Admin Successful login
@pytest.mark.order(2)
def test_admin_valid_login(page, base_url, config):
    login = LoginPage(page, base_url)
    login.open_login()

    time.sleep(2)

    creds = config["users"]["admin"]
    login.enter_username(creds["username"])
    login.enter_password(creds["password"])
    login.click_login()
    time.sleep(3)

    expect(login.exit_button, "Exit button not visible after admin login").to_be_visible()
    expect(login.admin_panel_button, "Admin panel link not visible").to_be_visible()
    expect(login.timesheet_panel_button, "Timesheet panel link not visible").to_be_visible()
    expect(login.performance_review_panel_button, "Performance Review panel link not visible").to_be_visible()
    expect(login.admin_profile_link, "Admin profile link not visible").to_be_visible()


# Logout
@pytest.mark.order(3)
def test_logout(page, base_url):
    login = LoginPage(page, base_url)

    # Click logout
    login.click_logout()
    time.sleep(2)


    # Wait for the modal to appear
    expect(login.logout_modal_title).to_be_visible()

    login.confirm_logout_button.click()

    time.sleep(2)

    # Assert returned to login page
    expect(login.username_input, "Username input is not visible").to_be_visible()
    expect(login.password_input, "Password input is not visible").to_be_visible()
    expect(login.login_button, "Login button is not visible").to_be_visible()

@pytest.mark.order(4)
def test_user_valid_login(page, base_url, config):
    login = LoginPage(page, base_url)
    login.open_login()
    time.sleep(2)

    creds = config["users"]["user"]
    login.enter_username(creds["username"])
    login.enter_password(creds["password"])
    login.click_login()

    time.sleep(2)

    expect(login.exit_button, "Exit button not visible after admin login").to_be_visible()
    expect(login.timesheet_panel_button, "Timesheet panel link not visible").to_be_visible()
    expect(login.performance_review_panel_button, "Performance Review panel link not visible").to_be_visible()
    expect(login.user_profile_link, "User profile link not visible").to_be_visible()
