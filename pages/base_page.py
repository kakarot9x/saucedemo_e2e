# pages/base_page.py
import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as exp
from selenium.webdriver.support.ui import WebDriverWait

log = logging.getLogger(__name__)

class BasePage:
    # Common Locators (placed here if used across many pages)
    CART_ICON_LOCATOR = (By.ID, "shopping_cart_container")
    CART_BADGE_LOCATOR = (By.XPATH, "//span[@class='shopping_cart_badge']")
    BURGER_BUTTON = (By.ID, "react-burger-menu-btn")
    BURGER_ITEMS = (By.CSS_SELECTOR, ".bm-item.menu-item")
    ALL_ITEMS_LINK_LOCATOR = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK_LOCATOR = (By.ID, "about_sidebar_link")
    LOGOUT_LINK_LOCATOR = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK_LOCATOR = (By.ID, "reset_sidebar_link")
    BURGER_MENU_CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")
    INVENTORY_ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Explicit wait with 10-second timeout

    #############################################
    #   Common Selenium actions
    #############################################
    def go_to_url(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def get_element_text(self, locator):
        return self.wait.until(exp.visibility_of_element_located(locator)).text

    def click_element(self, locator):
        """
        Waits for an element to be visible, then clickable, and then clicks it.
        """
        try:
            # First, wait for presence
            self.wait.until(exp.presence_of_element_located(locator))
            # Then, wait for clickability
            self.wait.until(exp.element_to_be_clickable(locator)).click()
            log.info(f"Element {locator} clicked")
        except Exception as e:
            log.error(f"Error clicking element with locator {locator}: {e}")
            raise

    def type_into_element(self, locator, text):
        element = self.wait.until(exp.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        log.info(f"'{text}' entered to element {locator}")

    def is_element_present(self, locator):
        try:
            self.wait.until(exp.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator):
        try:
            self.wait.until(exp.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    #############################################
    #   Common actions shared across pages
    #############################################
    def open_hamburger_menu(self):
        self.click_element(self.BURGER_BUTTON)
        self.wait.until(exp.visibility_of_element_located(self.BURGER_MENU_CLOSE_BUTTON))

    def close_hamburger_menu(self):
        self.click_element(self.BURGER_MENU_CLOSE_BUTTON)
        self.wait.until(exp.invisibility_of_element_located(self.BURGER_MENU_CLOSE_BUTTON))

    def logout(self):
        self.open_hamburger_menu()
        self.click_element(self.LOGOUT_LINK_LOCATOR)
