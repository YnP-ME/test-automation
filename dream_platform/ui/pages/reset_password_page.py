from dream_platform.ui.pages.base_page import BasePage

class ResetPasswordPage(BasePage):
    """Page object for the Reset Password page after clicking email link."""
    def __init__(self, page):
        super().__init__(page)

        # ---------- Page elements ----------
        self.header = page.locator("h1:text('Recover password')")
        self.new_password_label = page.locator("label:text('New password')")
        self.new_password_input = page.locator("input._input_1kmm2_1._input_size__md_1kmm2_32[type='text']" )
        self.save_password_button = page.locator("button:text('Save password')")

    # ---------- Actions ----------
    def enter_new_password(self, password):
        self.new_password_input.wait_for(state="visible", timeout=20000)
        self.new_password_input.click()
        self.new_password_input.fill(password)

    def click_save(self):
        self.save_password_button.click()
