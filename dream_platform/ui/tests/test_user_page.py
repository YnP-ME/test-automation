import time
from dream_platform.ui.pages.login_page import LoginPage
from dream_platform.ui.pages.user_page import UserPage
from playwright.sync_api import expect


def test_user_profile_page_visible(browser_page, base_url, login_as_user):
    """Check that user profile page elements are visible after login."""
    # Already logged in via fixture
    user = UserPage(browser_page, base_url)
    user.click_user_icon()

    # Assertions for header visibility
    expect(user.profile_header, "Profile header is not visible").to_be_visible()

    # Assertions for input fields visibility
    expect(user.first_name_input, "First name input is not visible").to_be_visible()
    expect(user.last_name_input, "Last name input is not visible").to_be_visible()
    expect(user.email_input, "Email input is not visible").to_be_visible()

    # Assertions for buttons visibility
    expect(user.change_password_button, "Change password button is not visible").to_be_visible()
    expect(user.save_changes_button, "Save changes button is not visible").to_be_visible()


def test_change_password_modal_elements(browser_page, base_url):
    """Check that change password modal elements are visible."""
    user = UserPage(browser_page, base_url)

    # Open change password modal
    user.click_change_password()
    time.sleep(1)  # Could replace with proper wait

    # Assertions for modal and its elements visibility
    expect(user.change_password_modal, "Change password modal is not visible").to_be_visible()
    expect(user.current_password_input, "Current password input is not visible").to_be_visible()
    expect(user.new_password_input, "New password input is not visible").to_be_visible()
    expect(user.save_password_button, "Save password button is not visible").to_be_visible()
    expect(user.cancel_password_button, "Cancel button is not visible").to_be_visible()

    # Close modal
    user.cancel_password()


def test_password_change_and_login(browser_page, base_url, config, restore_password):
    """Test password change workflow and login validation with old/new passwords."""
    login = LoginPage(browser_page, base_url)
    user = UserPage(browser_page, base_url)
    creds = config["users"]["user"]
    original_password = creds["password"]
    new_password = creds["new_pass"]

    # Change password → new
    user.click_user_icon()
    user.click_change_password()
    user.current_password_input.fill(original_password)
    user.new_password_input.fill(new_password)
    user.save_password_button.click()

    # Assertion for successful password change
    expect(user.password_change_success, "Password change success message not visible").to_be_visible()

    # Logout after password change
    login.click_logout()
    login.confirm_logout()

    # Login with new password → should succeed
    login.open_login()
    login.enter_username(creds["username"])
    login.enter_password(new_password)
    login.click_login()

    # Assertions for successful login with new password
    expect(login.exit_button, "Exit button not visible after login").to_be_visible()
    expect(login.timesheet_panel_button, "Timesheet panel link not visible").to_be_visible()
    expect(login.performance_review_panel_button, "Performance Review panel link not visible").to_be_visible()
    expect(login.user_profile_link, "User profile link not visible").to_be_visible()

    # Login with old password → should fail
    login.click_logout()
    login.confirm_logout()
    login.open_login()
    login.enter_username(creds["username"])
    login.enter_password(original_password)
    login.click_login()

    # Assertions for login failure with old password
    expect(login.invalid_login_error, "Invalid login error not visible").to_be_visible()
    expect(login.invalid_login_error, "Error text mismatch").to_have_text("Incorrect login or password")
