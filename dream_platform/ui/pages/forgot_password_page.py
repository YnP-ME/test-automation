from dream_platform.ui.pages.base_page import BasePage

class ForgotPasswordPage(BasePage):
    """Page object for the Forgot Password page."""

    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.url = f"{base_url}password-reset"

        # ---------- Page elements ----------
        self.header = page.locator("h1:text('Recover password')")
        self.description = page.locator(
            "p:text('Please enter your email address and we will send you instructions for obtaining your password.')"
        )
        self.email_input = page.locator("input[type='text']")
        self.restore_button = page.locator("button:text('Restore password')")
        self.success_message = page.get_by_text("We have sent you an email, if you have not received it, it may be because you have not registered on our platform.",exact=True)

    # ---------- Actions ----------
    def open(self):
        self.goto(self.url)

    def restore_password(self, email: str):
        self.email_input.fill(email)
        self.restore_button.click()