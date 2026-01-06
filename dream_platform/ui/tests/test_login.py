import time
import pytest
from playwright.sync_api import expect
from dream_platform.ui.pages.login_page import LoginPage
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
EMPLOYEE_USERNAME = os.getenv("EMPLOYEE_USERNAME")
EMPLOYEE_PASSWORD = os.getenv("EMPLOYEE_PASSWORD")

@pytest.mark.order(1)
def test_login_page_elements_before_login(browser_page, base_url):
    """Check that all login page elements are visible before login."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    # Assertions for page elements visibility
    expect(login.login_page_title, "Login page title is not visible").to_be_visible()
    expect(login.login_header_logo, "Company name is not visible on login page").to_be_visible()
    expect(login.username_input, "Username input is not visible").to_be_visible()
    expect(login.password_input, "Password input is not visible").to_be_visible()
    expect(login.login_button, "Login button is not visible").to_be_visible()
    expect(login.forgot_password_link,"Forgot password button is not visible").to_be_visible()

@pytest.mark.order(2)
def test_admin_valid_login(browser_page, base_url, config):
    """Admin can log in successfully and see expected elements."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    login.enter_username(ADMIN_USERNAME)
    login.enter_password(ADMIN_PASSWORD)
    login.click_login()

    # Assertions for admin login success
    expect(login.exit_button, "Exit button not visible after admin login").to_be_visible()
    expect(login.admin_panel_button, "Admin panel link not visible").to_be_visible()
    expect(login.timesheet_panel_button, "Timesheet panel link not visible").to_be_visible()
    expect(login.performance_review_panel_button, "Performance Review panel link not visible").to_be_visible()
    expect(login.admin_profile_link, "Admin profile link not visible").to_be_visible()

@pytest.mark.order(3)
def test_logout(browser_page, base_url):
    """Test logout functionality and returning to login page."""
    login = LoginPage(browser_page, base_url)

    # Click logout
    login.click_logout()
    time.sleep(1)

    # Wait for logout modal
    expect(login.logout_modal_title).to_be_visible()
    login.confirm_logout()

    # Assertions for returned login page
    expect(login.username_input, "Username input is not visible").to_be_visible()
    expect(login.password_input, "Password input is not visible").to_be_visible()
    expect(login.login_button, "Login button is not visible").to_be_visible()

@pytest.mark.order(4)
def test_invalid_login_wrong_username(browser_page, base_url, config):
    """Login should fail with wrong username."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    login.enter_username("wrong_username@gmail.com")
    login.enter_password(EMPLOYEE_PASSWORD)
    login.click_login()

    # Assertions for invalid login error
    expect(login.invalid_login_error).to_be_visible()
    expect(login.invalid_login_error).to_have_text("Incorrect login or password")

@pytest.mark.order(5)
def test_invalid_login_wrong_password(browser_page, base_url, config):
    """Login should fail with wrong password."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    login.enter_username(EMPLOYEE_USERNAME)
    login.enter_password("wrong_password")
    login.click_login()

    # Assertions for invalid login error
    expect(login.invalid_login_error).to_be_visible()
    expect(login.invalid_login_error).to_have_text("Incorrect login or password")

@pytest.mark.order(6)
def test_invalid_login_wrong_username_and_password(browser_page, base_url):
    """Login should fail with wrong username and password."""
    login = LoginPage(browser_page, base_url)
    login.open_login()
    login.enter_username("wrong_user")
    login.enter_password("wrong_password")
    login.click_login()

    # Assertions for invalid login error
    expect(login.invalid_login_error).to_be_visible()
    expect(login.invalid_login_error).to_have_text("Incorrect login or password")

@pytest.mark.order(7)
def test_user_valid_login(browser_page, base_url, config):
    """User can log in successfully and see expected elements."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    login.enter_username(EMPLOYEE_USERNAME)
    login.enter_password(EMPLOYEE_PASSWORD)
    login.click_login()

    # Assertions for user login success
    expect(login.exit_button, "Exit button not visible after login").to_be_visible()
    expect(login.timesheet_panel_button, "Timesheet panel link not visible").to_be_visible()
    expect(login.performance_review_panel_button, "Performance Review panel link not visible").to_be_visible()
    expect(login.user_profile_link, "User profile link not visible").to_be_visible()

@pytest.mark.order(8)
def test_cancel_logout(browser_page, base_url):
    """Test canceling logout keeps user on current page."""
    login = LoginPage(browser_page, base_url)

    # Click logout
    login.click_logout()
    expect(login.logout_modal_title).to_be_visible()

    login.cancel_logout_button.click()

    # Assertions for staying on the page
    expect(login.exit_button, "Exit button not visible after login").to_be_visible()
    expect(login.timesheet_panel_button, "Timesheet panel link not visible").to_be_visible()
    expect(login.performance_review_panel_button, "Performance Review panel link not visible").to_be_visible()
    expect(login.user_profile_link, "User profile link not visible").to_be_visible()

    #logout
    login.click_logout()
    login.confirm_logout()
