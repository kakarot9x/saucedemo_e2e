# pages/inventory_page.py
import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # <--- Add this import
from selenium.webdriver.support.ui import Select

from conftest import CONFIG
from constants import Urls
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.product_detail_page import ProductDetailPage

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    # Locators
    PRODUCT_TITLE_LOCATOR = (By.CSS_SELECTOR, ".title")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ADD_TO_CART_BUTTON_PREFIX = "add-to-cart-"
    REMOVE_BUTTON_PREFIX = "remove-"

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Urls.INVENTORY_URL

    def go_to_inventory_page(self):
        self.go_to_url(self.url)
        # Ensure product title is visible before proceeding
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLE_LOCATOR))

    def get_page_title(self):
        return self.get_element_text(self.PRODUCT_TITLE_LOCATOR)

    def sort_products_by(self, sort_option_value):
        """
        Sorts products using the dropdown.
        Possible values: 'az', 'za', 'lohi', 'hilo'
        """
        # Corrected line: Wait until the dropdown element is visible and then get it
        sort_dropdown_element = self.wait.until(EC.visibility_of_element_located(self.SORT_DROPDOWN))
        select = Select(sort_dropdown_element)  # Pass the WebElement to Select
        select.select_by_value(sort_option_value)

    def get_product_names(self):
        # Use explicit wait here too if elements might not be immediately present
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_NAMES))
        name_elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [elem.text for elem in name_elements]

    def get_product_prices(self):
        # Use explicit wait here too
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_PRICES))
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(elem.text.replace('$', '')) for elem in price_elements]

    def add_product_to_cart(self, product_name):
        button_id_suffix = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
        add_to_cart_locator = (By.ID, f"{self.ADD_TO_CART_BUTTON_PREFIX}{button_id_suffix}")
        self.click_element(add_to_cart_locator)  # This internally uses self.wait.until(EC.element_to_be_clickable)

    def remove_product_from_cart(self, product_name):
        button_id_suffix = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
        remove_locator = (By.ID, f"{self.REMOVE_BUTTON_PREFIX}{button_id_suffix}")
        self.click_element(remove_locator)  # This internally uses self.wait.until(EC.element_to_be_clickable)

    def get_product_button_text(self, product_name):
        button_id_suffix = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
        add_button_locator = (By.ID, f"{self.ADD_TO_CART_BUTTON_PREFIX}{button_id_suffix}")
        remove_button_locator = (By.ID, f"{self.REMOVE_BUTTON_PREFIX}{button_id_suffix}")

        # You need to wait for one of them to be visible, then get its text
        try:
            return self.wait.until(EC.visibility_of_element_located(add_button_locator)).text
        except:
            try:
                return self.wait.until(EC.visibility_of_element_located(remove_button_locator)).text
            except:
                return None  # Neither button is visible

    def click_product_name(self, product_name):
        """
        Clicks on the product name link to navigate to the product detail page.
        The actual clickable element is an <a> tag inside the inventory_item_name div.
        """
        # Updated XPath to target the clickable <a> tag within the div
        product_name_locator = (By.XPATH, f"//div[@class='inventory_item_name']/a[contains(text(), '{product_name}')]")

        for i in range(3):
            if self.is_element_present(product_name_locator):
                self.click_element(product_name_locator)
                break
            elif self.is_element_present(product_name_locator):
                self.click_element(product_name_locator)
                break
            else:
                logger.info(product_name + f" is not clickable or not present after {i}s")
                time.sleep(1)

        # Assuming ProductDetailPage is imported and correctly initialized
        return ProductDetailPage(self.driver)

    def navigate_to_cart(self):
        self.click_cart_icon()  # This internally uses self.wait.until(EC.element_to_be_clickable)
        return CartPage(self.driver)