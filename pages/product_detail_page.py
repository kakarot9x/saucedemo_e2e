# pages/product_detail_page.py
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


# from pages.inventory_page import InventoryPage # <--- REMOVE THIS LINE

class ProductDetailPage(BasePage):
    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, ".inventory_details_name")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".inventory_details_desc")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_details_price")
    BACK_TO_PRODUCTS_BUTTON = (By.ID, "back-to-products")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btn_primary.btn_inventory")
    REMOVE_FROM_CART_BUTTON = (By.CSS_SELECTOR, ".btn_secondary.btn_inventory")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_name(self):
        return self.get_element_text(self.PRODUCT_NAME)

    def get_product_description(self):
        return self.get_element_text(self.PRODUCT_DESCRIPTION)

    def get_product_price(self):
        price_text = self.get_element_text(self.PRODUCT_PRICE)
        return float(price_text.replace('$', ''))

    def click_add_to_cart(self):
        self.click_element(self.ADD_TO_CART_BUTTON)

    def click_remove_from_cart(self):
        self.click_element(self.REMOVE_FROM_CART_BUTTON)

    def click_back_to_products(self):
        # Import InventoryPage here, inside the method
        from pages.inventory_page import InventoryPage  # <--- MODIFIED LINE
        self.click_element(self.BACK_TO_PRODUCTS_BUTTON)
        return InventoryPage(self.driver)

    def is_add_to_cart_button_visible(self):
        return self.is_element_visible(self.ADD_TO_CART_BUTTON)

    def is_remove_from_cart_button_visible(self):
        return self.is_element_visible(self.REMOVE_FROM_CART_BUTTON)