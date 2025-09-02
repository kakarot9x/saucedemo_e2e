import json
import logging
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeServices
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager

from tests.data import User
from pages.login_page import LoginPage

log = logging.getLogger()
CONFIG = {}

# Command line options for pytest
def pytest_addoption(parser):
    """
    Adds custom command line options for env and browser selection.
    :param parser:
    """
    parser.addoption(
        "--env", action="store", default="stage",
        help="Environment for tests, (e.g., stage, product, dev)"
    )

    parser.addoption(
        "--browser", action="store", default="chrome",
        help="Browser for tests, (e.g., chrome, firefox, edge)"
    )

    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Option to run test in headless mode"
    )

# Fixture to load configuration
def pytest_configure(config):
    """
    Loads configuration from config.json based on the --env argument and share the global CONFIG dictionary
    :param config:
    :return:
    """
    env = config.getoption("--env")
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, encoding='utf-8') as config_file:
        config_data = json.load(config_file)

    # Select the configuration for specific env
    try:
        env_config_data = config_data['environments'][env]
    except KeyError as exc:
        raise pytest.UsageError(
            f"Env - '{env}' not found in the config.json"
            f"Available envs: {list(config_data['environments'].keys())}"
        ) from exc

    final_config = {k: v for k, v in config_data.items() if k != 'environments'}
    final_config.update(env_config_data)
    CONFIG.update(final_config)

    # create logs and screenshots path if not existing
    logs_dir = Path(__file__).parent / CONFIG['output_logs']
    logs_dir.mkdir(parents=True, exist_ok=True)
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_log_path = logs_dir/ f"test_run_{time_stamp}.log"
    config.option.log_file = str(new_log_path)

    screenshot_dir = Path(__file__).parent / CONFIG['output_screenshots']
    screenshot_dir.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("--browser").lower()
    env_name = request.config.getoption("--env").lower()
    headless = request.config.getoption("--headless")
    base_url = CONFIG['base_url']

    log.info("--"*50)
    log.info(f"Test environment: {env_name.upper()}, Browser: {browser_name.capitalize()}, Headless: {headless}, URL: {base_url}")
    log.info("--"*50)

    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        driver_path = ChromeDriverManager().install()
        log.debug(f"ChromeDriver: {driver_path}")
        services = ChromeServices(executable_path=driver_path)

        chrome_options.add_argument("--no-sandbox")
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        # --- Options to Make Automation Less Detectable ---
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # --- Preferences to Disable Pop-ups and Warnings ---
        prefs = {
            "credentials_enable_service": False,
            "password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "devtools.preferences.selfXssWarning": "false",
            "profile.default_content_setting_values.notifications": 1  # 1=Allow, 2=Block
        }
        chrome_options.add_experimental_option("prefs", prefs)
        web_driver = webdriver.Chrome(service=services, options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        web_driver = webdriver.Firefox(options=firefox_options)
    elif browser_name == "edge":
        edge_options = EdgeOptions()
        if headless:
            edge_options.add_argument("--headless")
        edge_options.add_argument("--window-size=1920,1080")
        web_driver = webdriver.Edge(options=edge_options)
    else:
        raise pytest.UsageError(f"Unsupported browser: '{browser_name}'. "
                                "Supported browsers: chrome, firefox, edge")

    # Set a consistent window size for all tests
    web_driver.maximize_window()
    web_driver.delete_all_cookies()

    yield web_driver

    # --- Teardown Phase ---
    if web_driver is not None:
        log.info("Closing browser session...")
        web_driver.quit()


# Function to capture test report and take screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Function to capture test report and take screenshot on failure
    :param item:
    :return:
    """
    outcome = yield
    report = outcome.get_result()

    setattr(item, "report", report)

    if report.when == "call" and report.failed:
        log.error(f"Test '{item.name}' failed. Taking screenshot...")
        #get driver instance to capture screenshot
        driver_inst = None
        for fixture_value in item.funcargs.values():
            if isinstance(fixture_value, WebDriver):
                driver_inst = fixture_value
                break
        if driver_inst:
            try:
                screenshot_name = f"FAIL_{item.name}"
                take_screenshot(driver=driver_inst, name=screenshot_name)
            except (IOError, OSError, RuntimeError) as e:
                log.error(f"Could not take screenshot on failed test '{item.name}': {e}")

def take_screenshot(driver, name: str = None):
    """
    Take screenshot with specific name
    :param driver:
    :param name:
    :return:
    """
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = Path(__file__).parent / CONFIG['output_screenshots'] / f"{name}_{time_stamp}.png"

    # save screenshot and log path
    try:
        driver.save_screenshot(str(file_path))
        log.info(f"Screenshot captured at: {file_path}")
    except Exception as e:
        log.error(f"Failed to capture screenshot for '{name}': {e}")

# Function for test logger
@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """
    Logs the start and end of each test function include the final status
    :param request:
    :return:
    """
    test_name = request.node.name
    log.info("--"*50)
    log.info(f"STARTING: {test_name}")
    log.info("--" * 50)

    start_time = datetime.now()

    yield

    # teardown step
    report = request.node.report
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    if report.when == "call":
        if report.passed:
            status = "PASSED"
        elif report.failed:
            status = "FAILED"
        elif report.skipped:
            status = "SKIPPED"
        else:
            status = "UNKNOWN"
    else:
        # This handles fixtures and other test stages
        status = f"FIXTURE_{report.when.upper()}_{report.outcome.upper()}"

    log.info("==" * 50)
    log.info("RESULT: '%s' is %s, Duration: %.2fs", test_name, status, duration)
    log.info("==" * 50)

@pytest.fixture(scope="function")
def login_page(driver):
    """Provides a LoginPage object for tests."""
    page = LoginPage(driver)
    page.go_to_login_page()
    logging.info("Navigated to login page")  # Log navigation
    return page


@pytest.fixture(scope="function")
def logged_in_page(driver):
    """
    Fixture to ensure a user is logged in before the test.
    Returns an InventoryPage object.
    """
    login_pg = LoginPage(driver)
    login_pg.go_to_login_page()
    # Ensure login method returns InventoryPage
    logging.info(f"Attempting to log in user: {User.STANDARD_USER['username']}")
    # Log login attempt
    inventory_pg = login_pg.login(User.STANDARD_USER["username"], User.STANDARD_USER["password"])
    # It's good practice to assert successful login here as part of fixture setup
    assert inventory_pg is not None, "Fixture: Failed to log in standard user."
    assert inventory_pg.get_current_url() == CONFIG['base_url'] + "inventory.html"
    logging.info("User successfully logged in and navigated to Inventory page")
    # Log successful login
    return inventory_pg


