from dream_platform.ui.pages.user_timesheet_page import TimesheetPage
from playwright.sync_api import expect


def test_timesheet_page_ui_elements(browser_page, base_url, login_as_user):
    """Check that Timesheet page elements are visible after login."""
    timesheet = TimesheetPage(browser_page, base_url)
    timesheet.open_timesheet_page()

    # Assertions for header visibility
    expect(timesheet.page_header, "Header is not visible").to_be_visible()
    expect(timesheet.timesheet_header, "Timesheet header is not visible").to_be_visible()
    expect(timesheet.back_button,"Back button is missing").to_be_visible()
    expect(timesheet.submit_timesheet_button, "Submit Timesheet button is not visible").to_be_visible()
    expect(timesheet.common_codes_section,"Missing project codes").to_be_visible()


def test_timesheet_add_and_submit_workflow(browser_page, base_url):
    """Test adding a timesheet entry and submitting the timesheet."""
    timesheet = TimesheetPage(browser_page, base_url)

    # Enter the code for Dream Platform
    timesheet.enter_project_code("OHV519")

    # Get text for the Dream Platform project
    dream_project_text = timesheet.get_project_text("OHV519")
    assert "Dream Platform Development" in dream_project_text, f"Expected 'Dream Platform Development' in project text, but got: {dream_project_text}"

    # Enter the code for Paid Vacation
    timesheet.enter_project_code("RQM317")

    # Get text for the Paid Vacation project
    paid_vacation_text = timesheet.get_project_text("RQM317")
    assert "Paid Vacation" in paid_vacation_text, f"Expected 'Paid Vacation' in project text, but got: {paid_vacation_text}"

