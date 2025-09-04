# pages/inventory_page.py
import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as exp
from selenium.webdriver.support.ui import Select

from constants import Urls
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.product_detail_page import ProductDetailPage

log = logging.getLogger(__name__)


class InventoryPage(BasePage):
    # Locators
    PRODUCT_TITLE_LOCATOR = (By.CSS_SELECTOR, ".title")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON_PREFIX = "add-to-cart-"
    REMOVE_BUTTON_PREFIX = "remove-"

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Urls.INVENTORY_URL

    def go_to_inventory_page(self):
        self.go_to_url(self.url)
        # Ensure product title is visible before process
        self.wait.until(exp.visibility_of_element_located(self.PRODUCT_TITLE_LOCATOR))

    def get_page_title(self):
        return self.get_element_text(self.PRODUCT_TITLE_LOCATOR)

    def get_burger_items(self):
        self.click_element(self.BURGER_BUTTON)
        items = self.driver.find_elements(*self.BURGER_ITEMS)
        log.info("List of actual Burger Menu Items: " + items)
        return [item.text for item in items]

    def sort_products_by(self, sort_option_value):
        """
        Sorts products using the dropdown.
        Possible values: 'az', 'za', 'lohi', 'hilo'
        """
        sort_dropdown_element = self.wait.until(exp.visibility_of_element_located(self.SORT_DROPDOWN))
        select = Select(sort_dropdown_element)
        select.select_by_value(sort_option_value)

    def get_product_names(self):
        self.wait.until(exp.presence_of_all_elements_located(self.PRODUCT_NAMES))
        name_elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [element.text for element in name_elements]

    def get_product_prices(self):
        self.wait.until(exp.presence_of_all_elements_located(self.PRODUCT_PRICES))
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(element.text.replace('$', '')) for element in price_elements]

    @staticmethod
    def update_product_button(product_name: str):
        return product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")

    def add_product_to_cart(self, product_name):
        """
        Finds and clicks the "Add to cart" button for a given product name.
        """
        button_id_suffix = self.update_product_button(product_name)
        add_locator = (By.ID, f"{self.ADD_TO_CART_BUTTON_PREFIX}{button_id_suffix}")
        self.click_element(add_locator)

    def remove_product_from_cart(self, product_name):
        button_id_suffix = self.update_product_button(product_name)
        remove_locator = (By.ID, f"{self.REMOVE_BUTTON_PREFIX}{button_id_suffix}")
        self.click_element(remove_locator)

    def get_product_button_text(self, product_name):
        button_id_suffix = self.update_product_button(product_name)
        add_button_locator = (By.ID, f"{self.ADD_TO_CART_BUTTON_PREFIX}{button_id_suffix}")
        remove_button_locator = (By.ID, f"{self.REMOVE_BUTTON_PREFIX}{button_id_suffix}")

        try:
            return self.wait.until(exp.visibility_of_element_located(add_button_locator)).text
        except:
            try:
                return self.wait.until(exp.visibility_of_element_located(remove_button_locator)).text
            except:
                return None  # No button is visible

    def click_product_name(self, product_name):
        """
        Clicks on the product name link to navigate to the product detail page.
        """
        product_name_locator = (By.XPATH, f"//div[@class='inventory_item_name']/a[contains(text(), '{product_name}')]")

        for i in range(3):
            if self.is_element_present(product_name_locator):
                self.click_element(product_name_locator)
                break
            elif self.is_element_present(product_name_locator):
                self.click_element(product_name_locator)
                break
            else:
                log.info(product_name + f" is not clickable or not present after {i}s")
                time.sleep(1)

        # Assuming ProductDetailPage is imported and correctly initialized
        return ProductDetailPage(self.driver)

    def get_cart_count(self):
        try:
            cart_badge = self.wait.until(exp.visibility_of_element_located(self.CART_BADGE_LOCATOR))
            return int(cart_badge.text)
        except TimeoutException:
            return 0  # Cart is empty
        except ValueError:
            return 0  # In case text is not a number

    def click_cart_icon(self):
        self.click_element(self.CART_ICON_LOCATOR)

    def navigate_to_cart(self):
        self.click_element(self.CART_ICON_LOCATOR)
        return CartPage(self.driver)
