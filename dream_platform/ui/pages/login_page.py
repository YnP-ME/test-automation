from dream_platform.ui.pages.base_page import BasePage

class LoginPage(BasePage):
    """Page object model for the login page."""

    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.url = f"{base_url}login"

        # ---------- Login page elements ----------
        self.login_page_title = page.locator(".font-family-title")
        self.login_header_logo = page.locator(".container-wrapper")
        self.username_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.get_by_role("button", name="Login")
        self.admin_panel_button = page.get_by_text("Admin", exact=True)
        self.timesheet_panel_button = page.get_by_text("timesheet")
        self.performance_review_panel_button = page.get_by_text("My Performance Review")
        self.exit_button = page.get_by_role("button", name="Exit")
        self.admin_profile_link = page.get_by_role("link", name="Test Admin", exact=True)
        self.user_profile_link = page.get_by_role("link", name="Test Employee")
        self.logout_modal_title = page.get_by_text("Are you sure you want to logout?")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.confirm_logout_button = page.get_by_role("button", name="Logout", exact=True)
        self.cancel_logout_button = page.get_by_role("button", name="Cancel", exact=True)
        self.invalid_login_error = page.locator("p:text('Incorrect login or password')")

    # ---------- Page actions ----------
    def open_login(self):
        """Navigate to the login page."""
        return self.goto(self.url)

    def enter_username(self, username):
        """Fill in the username field."""
        self.username_input.fill(username)

    def enter_password(self, password):
        """Fill in the password field."""
        self.password_input.fill(password)

    def click_login(self):
        """Click the login button."""
        self.login_button.click()

    def click_logout(self):
        """Click the exit button to start logout."""
        self.exit_button.click()

    def confirm_logout(self):
        """Confirm logout in the modal."""
        self.confirm_logout_button.click()
