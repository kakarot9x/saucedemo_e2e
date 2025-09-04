# pages/login_page.py
import logging

from selenium.webdriver.common.by import By

from constants import Urls
from pages.base_page import BasePage

log = logging.getLogger(__name__)

class LoginPage(BasePage):
    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE_LOCATOR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Urls.LOGIN_URL

    def go_to_login_page(self):
        self.go_to_url(self.url)

    def enter_username(self, username):
        self.type_into_element(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        self.type_into_element(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)

    def login(self, username, password):
        from pages.inventory_page import InventoryPage
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        if self.get_current_url() == Urls.INVENTORY_URL:
            return InventoryPage(self.driver)
        return None  # login failed

    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE_LOCATOR)

    def verify_error_message(self, expected_message):
        error_msg = self.get_error_message()
        assert error_msg == expected_message, f"Expected error '{expected_message}' but got '{error_msg}'"

    def verify_on_login_page(self):
        assert self.get_current_url() == self.url, \
            f"Expected to be on login page ({self.url}), but got {self.get_current_url()}"
        assert self.is_element_visible(self.LOGIN_BUTTON), "Login button not visible on login page."