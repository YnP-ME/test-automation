import os
import pytest
import yaml
from playwright.sync_api import sync_playwright

# ---- Load configs from YAML ----
def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

# ---- Add custom CLI option for pytest ----
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Environments: local, staging, production"
    )

# ---- Fixture: base_url for the test session ----
@pytest.fixture(scope="session")
def base_url(request):
    config = load_config()
    cli_env = request.config.getoption("--env")
    env_var = os.getenv("TEST_ENV")
    default_env = config.get("default", "local")

    active_env = cli_env or env_var or default_env
    url = config["environments"][active_env]

    print(f"\nRunning tests against: {active_env} → {url}")
    return url

# ---- Fixture: Playwright page ----
@pytest.fixture(scope="session")
def page(request):
    browser_name = request.config.getoption("browser")
    if isinstance(browser_name, list):
        browser_name = browser_name[0]

    with sync_playwright() as p:
        if browser_name == "chromium":
            browser = p.chromium.launch(headless=False)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=False)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=False)
        else:
            raise ValueError(f"Unknown browser: {browser_name}")

        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

# ---- Fixture: Return config dict ----
@pytest.fixture(scope="session")
def config():
    return load_config()
