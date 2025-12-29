import os
import msal
import pytest
import yaml
from playwright.sync_api import sync_playwright, expect
from dream_platform.ui.pages.login_page import LoginPage
import requests
from datetime import datetime, timezone, timedelta
import time

# ---------- Load config ----------
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)

# ---------- CLI options ----------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chromium", help="Browser: chromium, firefox, webkit")
    parser.addoption("--env", action="store", help="Environment name")

# ---------- Fixtures ----------
@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="session")
def base_url(request, config):
    cli_env = request.config.getoption("--env")
    env_var = os.getenv("TEST_ENV")
    default_env = config.get("default", "production")
    active_env = cli_env or env_var or default_env
    url = config["environments"][active_env]
    print(f"\nRunning tests against: {active_env} → {url}")
    return url

@pytest.fixture(scope="session")
def browser_page(request):
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
    login = LoginPage(browser_page, base_url)
    login.open_login()
    creds = config["users"]["user"]
    login.enter_username(creds["username"])
    login.enter_password(creds["password"])
    login.click_login()
    expect(login.exit_button).to_be_visible()

@pytest.fixture
def login_as_admin(browser_page, base_url, config):
    login = LoginPage(browser_page, base_url)
    login.open_login()
    creds = config["users"]["admin"]
    login.enter_username(creds["username"])
    login.enter_password(creds["password"])
    login.click_login()
    expect(login.admin_panel_button).to_be_visible()

# ---------- Graph API for Outlook ----------
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

def get_last_reset_email_graph(user_email: str, max_wait=60):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders/Inbox/messages?$top=20"

    from datetime import datetime, timezone, timedelta
    import requests
    import time

    start_time = datetime.now(timezone.utc) - timedelta(seconds=5)  # small buffer
    end_time = (start_time + timedelta(seconds=max_wait)).timestamp()

    while datetime.now(timezone.utc).timestamp() < end_time:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        messages = resp.json().get("value", [])

        for msg in messages:
            sender = msg.get("from", {}).get("emailAddress", {}).get("address", "").lower()
            received = msg.get("receivedDateTime")
            if not sender or not received:
                continue

            msg_time = datetime.fromisoformat(received.replace("Z", "+00:00"))
            print("DEBUG EMAIL:", sender, msg_time)  # debug

            if "inquiries@quantumone.ae" in sender and msg_time > start_time:
                return msg["body"]["content"]

        time.sleep(1)

    raise AssertionError("No new password reset email received")
