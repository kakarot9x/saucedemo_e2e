# pages/checkout_page.py
from selenium.webdriver.common.by import By
import logging

from constants import Urls
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class CheckoutInfoPage(BasePage):
     # Locators
     FIRST_NAME_FIELD = (By.ID, "first-name")
     LAST_NAME_FIELD = (By.ID, "last-name")
     ZIP_POSTAL_CODE_FIELD = (By.ID, "postal-code")
     CONTINUE_BUTTON = (By.ID, "continue")
     CANCEL_BUTTON = (By.ID, "cancel")
     ERROR_MESSAGE_LOCATOR = (By.CSS_SELECTOR, "[data-test='error']")

     def __init__(self, driver):
         super().__init__(driver)
         self.url = Urls.CHECKOUT_STEP_ONE_URL

     def fill_your_information(self, first_name, last_name, zip_code):
         self.type_into_element(self.FIRST_NAME_FIELD, first_name)
         self.type_into_element(self.LAST_NAME_FIELD, last_name)
         self.type_into_element(self.ZIP_POSTAL_CODE_FIELD, zip_code)

     def click_continue(self):
         self.click_element(self.CONTINUE_BUTTON)
         if self.get_current_url() == Urls.CHECKOUT_STEP_TWO_URL:
            return CheckoutOverviewPage(self.driver)
         return None # In case of validation error

     def click_cancel(self):
        self.click_element(self.CANCEL_BUTTON)
        # Returns to inventory page

     def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE_LOCATOR)

     def is_error_message_visible(self):
        return self.is_element_visible(self.ERROR_MESSAGE_LOCATOR)


class CheckoutOverviewPage(BasePage):
     # Locators
     FINISH_BUTTON = (By.ID, "finish")
     CANCEL_BUTTON = (By.ID, "cancel")
     ITEM_TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label")
     TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label")
     TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label")
     CART_ITEM_LABELS = (By.CSS_SELECTOR, ".cart_item_label")
     CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
     INVENTORY_ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")

     def __init__(self, driver):
         super().__init__(driver)
         self.url = Urls.CHECKOUT_STEP_TWO_URL

     def get_item_total(self):
        text = self.get_element_text(self.ITEM_TOTAL_LABEL)
        return float(text.replace("Item total: $", ""))

     def get_tax(self):
         text = self.get_element_text(self.TAX_LABEL)
         return float(text.replace("Tax: $", ""))

     def get_total(self):
         text = self.get_element_text(self.TOTAL_LABEL)
         return float(text.replace("Total: $", ""))

     def get_item_details(self):
         item_details = []
         items = self.driver.find_elements(*self.CART_ITEM_LABELS)
         for item in items:
             name = item.find_element(*self.INVENTORY_ITEM_NAME).text
             price = float(item.find_element(*self.INVENTORY_ITEM_PRICE).text.replace('$', ''))
             logger.info(f"Product name: {name}, price: {price}")
             item_details.append({"name": name, "price": price})
         return item_details

     def click_finish(self):
         self.click_element(self.FINISH_BUTTON)
         return CheckoutCompletePage(self.driver)

     def click_cancel(self):
         self.click_element(self.CANCEL_BUTTON)
         # Returns to inventory page

class CheckoutCompletePage(BasePage):
     # Locators
     COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
     COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")
     BACK_HOME_BUTTON = (By.ID, "back-to-products")

     def __init__(self, driver):
         super().__init__(driver)
         self.url = Urls.CHECKOUT_COMPLETE_URL

     def get_complete_header_text(self):
        return self.get_element_text(self.COMPLETE_HEADER)

     def get_complete_text_message(self):
        return self.get_element_text(self.COMPLETE_TEXT)

     def click_back_home(self):
        self.click_element(self.BACK_HOME_BUTTON)
        # Returns to inventory page