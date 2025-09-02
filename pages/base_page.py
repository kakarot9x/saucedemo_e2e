# pages/base_page.py
import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

log = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Explicit wait with 10-second timeout

    def go_to_url(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def get_element_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def click_element(self, locator):
        """
        Waits for an element to be visible, then clickable, and then clicks it.
        """
        try:
            # First, wait for presence and visibility
            self.wait.until(EC.visibility_of_element_located(locator))
            # Then, wait for clickability
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except Exception as e:
            print(f"Error clicking element with locator {locator}: {e}")
            raise  # Re-raise the exception to propagate the failure

    def type_into_element(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def is_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_cart_count(self):
        try:
            cart_badge = self.wait.until(EC.visibility_of_element_located(self.CART_BADGE_LOCATOR))
            return int(cart_badge.text)
        except TimeoutException:
            return 0  # Cart is empty, no badge displayed
        except ValueError:
            return 0  # In case text is not a number, e.g., if it's '!'

    # Common Locators (can be placed here if used across many pages)
    CART_ICON_LOCATOR = ("id", "shopping_cart_container")
    CART_BADGE_LOCATOR = ("xpath", "//span[@class='shopping_cart_badge']")
    HAMBURGER_MENU_LOCATOR = ("id", "react-burger-menu-btn")
    ALL_ITEMS_LINK_LOCATOR = ("id", "inventory_sidebar_link")
    ABOUT_LINK_LOCATOR = ("id", "about_sidebar_link")
    LOGOUT_LINK_LOCATOR = ("id", "logout_sidebar_link")
    RESET_APP_STATE_LINK_LOCATOR = ("id", "reset_sidebar_link")
    BURGER_MENU_CLOSE_BUTTON = ("id", "react-burger-cross-btn")

    def click_cart_icon(self):
        self.click_element(self.CART_ICON_LOCATOR)

    def open_hamburger_menu(self):
        self.click_element(self.HAMBURGER_MENU_LOCATOR)
        self.wait.until(EC.visibility_of_element_located(self.BURGER_MENU_CLOSE_BUTTON))  # Wait for menu to open

    def close_hamburger_menu(self):
        self.click_element(self.BURGER_MENU_CLOSE_BUTTON)
        self.wait.until(EC.invisibility_of_element_located(self.BURGER_MENU_CLOSE_BUTTON))  # Wait for menu to close

    def logout(self):
        self.open_hamburger_menu()
        self.click_element(self.LOGOUT_LINK_LOCATOR)

    def reset_app_state(self):
        self.open_hamburger_menu()
        self.click_element(self.RESET_APP_STATE_LINK_LOCATOR)
        self.close_hamburger_menu()