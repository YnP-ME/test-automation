from dream_platform.ui.pages.base_page import BasePage

class UserPage(BasePage):
    """Page object model for the user profile page."""

    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.page = page

        # ---------- Locators ----------
        # Main profile page
        self.user_profile_link = page.get_by_role("link", name="Employee")
        self.profile_header = page.locator("h1:text('Profile Settings')")  # <h1> header
        self.first_name_input = page.locator("label:text('First name:') + div input")
        self.last_name_input = page.locator("label:text('Last name:') + div input")
        self.email_input = page.locator("input[disabled][value*='@']")  # email input
        self.change_password_button = page.locator("button:text('Change password')")
        self.save_changes_button = page.locator("button:text('Save changes')")

        # Change Password modal
        self.change_password_modal = page.locator(
            "div.rounded-2xl:has(h3:text('Change Password'))"
        )
        # Inputs inside modal
        self.current_password_input = self.change_password_modal.locator(
            "label:text('Current password:') + div input"
        )
        self.new_password_input = self.change_password_modal.locator(
            "label:text('New password:') + div input"
        )
        # Buttons inside modal
        self.save_password_button = self.change_password_modal.locator(
            "button:text('Save')"
        )
        self.cancel_password_button = self.change_password_modal.locator(
            "button:text('Cancel')"
        )
        # Success message after password change
        self.password_change_success = page.locator(
            "div._success_content__wrapper_5zecm_1 h3:text('Password was successfully changed')"
        )

    # ---------- Actions ----------
    def click_user_icon(self):
        """Click the user profile link to open profile page."""
        self.user_profile_link.click()

    def click_change_password(self):
        """Open the change password modal."""
        self.change_password_button.wait_for(state="visible")
        self.change_password_button.click()

    def click_save_changes(self):
        """Click the save changes button on profile page."""
        self.save_changes_button.click()

    def fill_change_password(self, current, new):
        """Fill the current and new password inputs in the modal."""
        self.current_password_input.fill(current)
        self.new_password_input.fill(new)

    def save_password(self):
        """Click the save button in the change password modal."""
        self.save_password_button.click()

    def cancel_password(self):
        """Click the cancel button in the change password modal."""
        self.cancel_password_button.click()
