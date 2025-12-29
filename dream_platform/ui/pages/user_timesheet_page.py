from dream_platform.ui.pages.base_page import BasePage


class TimesheetPage(BasePage):
    """Page object model for the timesheet page."""

    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.url = f"{base_url}timesheet"

        # ---------- Timesheet page elements ----------
        self.timesheet_header = page.locator("h1:has-text('Timesheet')")
        self.add_entry_button = page.get_by_role("button", name="Add Entry")
        self.submit_timesheet_button = page.get_by_role("button", name="Submit Timesheet")

        # Timesheet table columns
        self.timesheet_table = page.locator("table#timesheet")
        self.date_column = page.locator("table#timesheet th:has-text('Date')")
        self.hours_column = page.locator("table#timesheet th:has-text('Hours')")
        self.project_column = page.locator("table#timesheet th:has-text('Project')")

        # Add entry modal/form
        self.entry_date_input = page.locator("input[name='entry_date']")
        self.entry_hours_input = page.locator("input[name='entry_hours']")
        self.entry_project_select = page.locator("select[name='entry_project']")
        self.save_entry_button = page.get_by_role("button", name="Save")
        self.cancel_entry_button = page.get_by_role("button", name="Cancel")

        # Submission success message
        self.submission_success_message = page.locator("text=Timesheet submitted successfully")

    # ---------- Page actions ----------
    def open_timesheet_page(self):
        """Navigate to the timesheet page."""
        return self.goto(self.url)

    def click_add_entry(self):
        """Click the 'Add Entry' button to open the entry form."""
        self.add_entry_button.click()

    def fill_entry_form(self, date, hours, project):
        """Fill in the timesheet entry form."""
        self.entry_date_input.fill(date)
        self.entry_hours_input.fill(hours)
        self.entry_project_select.select_option(project)

    def save_entry(self):
        """Click the 'Save' button to save the timesheet entry."""
        self.save_entry_button.click()

    def cancel_entry(self):
        """Click the 'Cancel' button to close the entry form."""
        self.cancel_entry_button.click()

    def submit_timesheet(self):
        """Click the 'Submit Timesheet' button."""
        self.submit_timesheet_button.click()
