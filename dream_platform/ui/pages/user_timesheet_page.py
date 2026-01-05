from dream_platform.ui.pages.base_page import BasePage


class TimesheetPage(BasePage):
    """Page object model for the timesheet page."""

    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.url = f"{base_url}timesheet"

        # ---------- Timesheet page elements ----------
        self.page_header = page.locator("header.container-wrapper")
        self.timesheet_header = page.locator("h1:has-text('Timesheet')")
        self.back_button = page.get_by_role("button", name="Back")
        self.timesheet_form = page.locator('form:has(button[type="submit"]:has-text("Submit Timesheet"))')
        self.project_code_input = page.locator('input[name="projectCode"][placeholder="Add project code"]')
        self.submit_timesheet_button = page.get_by_role("button", name="Submit Timesheet")
        self.week_table = page.locator("div.grid.grid-cols-6")
        self.total_hours = page.locator("div.pt-5.flex.items-center.justify-center span")
        self.common_codes_section = page.locator("p:has-text('Common Codes:')")

        # Locate by exact text
        self.paid_vacation_button = page.locator("button", has_text="RQM317: Paid Vacation")
        self.sick_leave_button = page.locator("button", has_text="BDL757: Sick Leave")

        # Submission success message
        self.submission_success_message = page.locator("text=Timesheet submitted successfully")

    # ---------- Page actions ----------
    def open_timesheet_page(self):
        """Navigate to the timesheet page."""
        return self.goto(self.url)

    def enter_project_code(self, code: str):
        """
        Clicks the project code input and types the code.
        """
        self.project_code_input.click()
        self.project_code_input.fill(code)
        self.project_code_input.press("Enter")

    def get_project_text(self, code: str) -> str:
        """
        Returns the full text of the project row with the given project code.
        Example: "OHV519"
        """
        # Locate the row by the exact project code
        project_row_locator = self.page.locator(f'div.flex.justify-between.items-center span:has-text("{code}")')
        project_row_locator.wait_for(state="visible")
        return project_row_locator.inner_text()



