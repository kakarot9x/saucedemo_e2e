# tests/test_authentication.py
import logging

import pytest

from constants import Urls
from tests.data import User, ExpectedMessages

# Get logger instance
logger = logging.getLogger(__name__)


class TestAuthentication:
     def test_successful_login_standard_user(self, login_page):
         """AUTH-001: Verify standard user can successfully log in."""
         logger.info("Starting test: Successful Login - Standard User") # Log test start
         inventory_page = login_page.login(User.STANDARD_USER["username"], User.STANDARD_USER["password"])
         assert inventory_page is not None, "Login failed for standard_user."
         assert inventory_page.get_current_url() == Urls.INVENTORY_URL
         assert inventory_page.get_page_title() == "Products"
         logger.info("Test 'Successful Login - Standard User' PASSED.") # Log test pass

     def test_successful_login_problem_user(self, login_page):
         """AUTH-002: Verify problem user can log in."""
         inventory_page = login_page.login(User.PROBLEM_USER["username"], User.PROBLEM_USER["password"])
         assert inventory_page is not None, "Login failed for problem_user."
         assert inventory_page.get_current_url() == Urls.INVENTORY_URL
         assert inventory_page.get_page_title() == "Products"

     def test_successful_login_performance_glitch_user(self, login_page):
         """AUTH-003: Verify performance glitch user can log in."""
         import time
         start_time = time.time()
         inventory_page = login_page.login(User.PERFORMANCE_GLITCH_USER["username"],
         User.PERFORMANCE_GLITCH_USER["password"])
         end_time = time.time()
         assert inventory_page is not None, "Login failed for performance_glitch_user."
         assert inventory_page.get_current_url() == Urls.INVENTORY_URL
         assert inventory_page.get_page_title() == "Products"
         assert (end_time - start_time) > 2.0, "Performance glitch user logged in too fast!"

     @pytest.mark.parametrize("username, password, expected_error", [
         (User.LOCKED_OUT_USER["username"], User.LOCKED_OUT_USER["password"], ExpectedMessages.ERROR_LOCKED_OUT_USER),
         # AUTH-004
         (User.STANDARD_USER["username"], "wrong_password", ExpectedMessages.ERROR_INVALID_CREDENTIALS), # AUTH-005
         ("non_existent_user", "secret_sauce", ExpectedMessages.ERROR_INVALID_CREDENTIALS), # AUTH-006
         ("", User.STANDARD_USER["password"], ExpectedMessages.ERROR_USERNAME_REQUIRED), # AUTH-007
         (User.STANDARD_USER["username"], "", ExpectedMessages.ERROR_PASSWORD_REQUIRED), # AUTH-008
         ("", "", ExpectedMessages.ERROR_USERNAME_REQUIRED), # AUTH-009
     ])
     def test_invalid_login_scenarios(self, login_page, username, password, expected_error):
         """
         Covers AUTH-004, AUTH-005, AUTH-006, AUTH-007, AUTH-008, AUTH-009:
         Verify various invalid login attempts result in correct error messages and stay on login page.
         """
         logger.info(f"Starting test: Invalid Login Scenario for user '{username}'") # Log test start
         login_page.login(username, password)
         login_page.verify_on_login_page()
         login_page.verify_error_message(expected_error)
         logger.info(f"Test 'Invalid Login Scenario for user '{username}' PASSED.") # Log test pass

