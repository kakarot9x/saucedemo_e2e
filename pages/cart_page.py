# pages/cart_page.py
from selenium.webdriver.common.by import By

from constants import Urls
from pages.base_page import BasePage
from pages.checkout_page import CheckoutInfoPage

class CartPage(BasePage):
    # Locators
    YOUR_CART_TITLE = (By.CSS_SELECTOR, ".title")
    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTON_PREFIX = "remove-sauce-labs-"

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Urls.CART_URL

    def go_to_cart_page(self):
        self.go_to_url(self.url)
        self.wait.until(self.is_element_visible(self.YOUR_CART_TITLE))

    def get_cart_item_names(self):
        item_name_elements = self.driver.find_elements(*self.INVENTORY_ITEM_NAME)
        return [elem.text for elem in item_name_elements]

    def get_cart_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEM))

    def remove_product_from_cart(self, product_name):
        # This locator relies on the specific ID generation on the page.
        # A more robust way might be to find the item by name and then find its sibling button.
        button_id_suffix = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
        remove_button_locator = (By.ID, f"remove-{button_id_suffix}")
        self.click_element(remove_button_locator)

    def click_checkout(self):
        self.click_element(self.CHECKOUT_BUTTON)
        return CheckoutInfoPage(self.driver)

    def click_continue_shopping(self):
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
        # This will navigate back to inventory
