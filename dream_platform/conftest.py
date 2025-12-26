import sys
import os
import time

import msal
import requests

from dream_platform.utils.outlook_imap_oauth import login_outlook_imap_app_only

# Add project root to Python path so imports work
sys.path.append(os.path.dirname(__file__))
import email
import pytest
import yaml
from playwright.sync_api import sync_playwright, expect
from dream_platform.ui.pages.login_page import LoginPage
from dream_platform.ui.pages.user_page import UserPage


# ---------- Load config from YAML ----------
def load_config():
    """Load test configuration from config/config.yaml."""
    config_path = os.path.join(
        os.path.dirname(__file__),
        "config",
        "config.yaml"
    )
    with open(config_path) as f:
        return yaml.safe_load(f)


# ---------- Pytest CLI options ----------
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser: chromium, firefox, webkit"
    )
    parser.addoption(
        "--env",
        action="store",
        help="Environment name"
    )


# ---------- Fixtures ----------
@pytest.fixture(scope="session")
def config():
    """Return the loaded configuration for the test session."""
    return load_config()


@pytest.fixture(scope="session")
def base_url(request, config):
    """Determine the base URL for the tests based on CLI/env/default."""
    cli_env = request.config.getoption("--env")
    env_var = os.getenv("TEST_ENV")
    default_env = config.get("default", "production")

    active_env = cli_env or env_var or default_env
    url = config["environments"][active_env]

    print(f"\nRunning tests against: {active_env} → {url}")
    return url


@pytest.fixture(scope="session")
def browser_page(request):
    """Launch browser, provide page object, and cleanup after tests."""
    browser_name = request.config.getoption("--browser")

    playwright = sync_playwright().start()
    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=False)
    else:
        raise ValueError(f"Unknown browser: {browser_name}")

    context = browser.new_context()
    page = context.new_page()

    # Cleanup after all tests
    def teardown():
        page.close()
        context.close()
        browser.close()
        playwright.stop()

    request.addfinalizer(teardown)
    return page


# ---------- Login fixtures ----------
@pytest.fixture
def login_as_user(browser_page, base_url, config):
    """Log in as a regular user and verify login success."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    creds = config["users"]["user"]
    login.enter_username(creds["username"])
    login.enter_password(creds["password"])
    login.click_login()

    # Verify login succeeded
    expect(login.exit_button, "User exit button not visible after login").to_be_visible()


@pytest.fixture
def login_as_admin(browser_page, base_url, config):
    """Log in as admin and verify login success."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    creds = config["users"]["admin"]
    login.enter_username(creds["username"])
    login.enter_password(creds["password"])
    login.click_login()

    # Verify login succeeded
    expect(login.admin_panel_button, "Admin panel button not visible after login").to_be_visible()

@pytest.fixture
def restore_password(browser_page, base_url, config):
    """
    Restores original user password after test.
    Prevents breaking other tests that rely on default credentials.
    """
    creds = config["users"]["user"]
    original_password = creds["password"]
    new_password = creds["new_pass"]

    yield  # ----- TEST RUNS HERE -----

    try:
        login = LoginPage(browser_page, base_url)
        user = UserPage(browser_page, base_url)

        login.open_login()
        login.enter_username(creds["username"])
        login.enter_password(new_password)
        login.click_login()

        if user.user_icon.is_visible():
            user.click_user_icon()
            user.click_change_password()
            user.current_password_input.fill(new_password)
            user.new_password_input.fill(original_password)
            user.save_password_button.click()
            expect(user.password_change_success).to_be_visible()

            login.click_logout()
            login.confirm_logout()
    except Exception:
        print("Password restore skipped")

GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"

def get_access_token():
    client_id = os.environ["AZURE_CLIENT_ID"]
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}"
    )

    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise Exception(f"Failed to get access token: {result}")

    return result["access_token"]



@pytest.fixture
def last_password_reset_email():
    def _get_last_email(user_email: str, max_wait=120):
        token = get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{GRAPH_ENDPOINT}/users/{user_email}/mailFolders/Inbox/messages?$top=20"

        start_time = time.time()

        while time.time() - start_time < max_wait:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            messages = resp.json().get("value", [])

            for msg in messages:
                sender = msg["from"]["emailAddress"]["address"].lower()
                received = msg["receivedDateTime"]

                msg_time = time.mktime(
                    time.strptime(
                        received.replace("Z","").split('.')[0],
                        "%Y-%m-%dT%H:%M:%S"
                    )
                )

                if sender == "inquiries@quantumone.ae" and msg_time > start_time:
                    return msg["body"]["content"]

            time.sleep(5)

        raise AssertionError("No NEW password reset email received")
    return _get_last_email