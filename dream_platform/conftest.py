import os
import pytest
import yaml
from playwright.sync_api import sync_playwright

# ---- Load configs from YAML ----
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)

# ---- Add custom CLI option for pytest ----
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Environments: local, staging, production"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser: chromium, firefox, webkit"
    )

# ---- Fixture: base_url for the test session ----
# Base URL fixture
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

# Page fixture with proper cleanup
@pytest.fixture(scope="session")
def page(request):
    browser_name = request.config.getoption("browser")

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

    # Ensure cleanup after all tests
    def teardown():
        page.close()
        context.close()
        browser.close()
        playwright.stop()

    request.addfinalizer(teardown)
    return page

# Config fixture
@pytest.fixture(scope="session")
def config():
    return load_config()