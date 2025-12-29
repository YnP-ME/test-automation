from dream_platform.ui.pages.user_timesheet_page import TimesheetPage
from playwright.sync_api import expect


def test_timesheet_page_ui_elements(browser_page, base_url, login_as_user):
    """Check that Timesheet page elements are visible after login."""
    timesheet = TimesheetPage(browser_page, base_url)
    timesheet.open_timesheet_page()

    # Assertions for header visibility
    expect(timesheet.timesheet_header, "Timesheet header is not visible").to_be_visible()

    # Assertions for buttons visibility
    expect(timesheet.add_entry_button, "Add Entry button is not visible").to_be_visible()
    expect(timesheet.submit_timesheet_button, "Submit Timesheet button is not visible").to_be_visible()

    # Assertions for table columns visibility
    expect(timesheet.date_column, "Date column is not visible").to_be_visible()
    expect(timesheet.hours_column, "Hours column is not visible").to_be_visible()
    expect(timesheet.project_column, "Project column is not visible").to_be_visible()


def test_timesheet_add_and_submit_workflow(browser_page, base_url):
    """Test adding a timesheet entry and submitting the timesheet."""
    timesheet = TimesheetPage(browser_page, base_url)
    timesheet.open_timesheet_page()

    # Open add entry modal/form
    timesheet.add_entry_button.click()

    # Fill timesheet entry fields
    timesheet.entry_date_input.fill("2025-12-24")
    timesheet.entry_hours_input.fill("8")
    timesheet.entry_project_select.select_option("Project A")

    # Save entry
    timesheet.save_entry_button.click()

    # Assertion for new entry visible in table
    expect(timesheet.timesheet_table, "New timesheet entry not visible").to_contain_text("Project A")

    # Submit timesheet
    timesheet.submit_timesheet_button.click()

    # Assertion for submission success message
    expect(timesheet.submission_success_message, "Timesheet submission success message not visible").to_be_visible()
