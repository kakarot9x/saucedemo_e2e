# tests/test_cart_persistence.py
import logging

from constants import Urls
from tests.data import Products, User, CheckoutInfo, ExpectedMessages
from pages.login_page import LoginPage

log = logging.getLogger(__name__)


class TestE2ECheckOut:
    def test_cart_state_after_logout_and_relogin(self, driver):
        """CART-PERSIST-001: Verify cart is cleared after logout/re-login."""
        # Log in and add item
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        inventory_page = login_page.login(User.STANDARD_USER["username"], User.STANDARD_USER["password"])
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_ONESIE)
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_FLEECE_JACKET)
        assert inventory_page.get_cart_count() == 3

        # Logout
        inventory_page.logout()
        login_page.verify_on_login_page()

        # Re-login
        inventory_page_after_relogin = login_page.login(User.STANDARD_USER["username"], User.STANDARD_USER["password"])
        assert inventory_page_after_relogin.get_cart_count() == 3, "Cart was cleared after logout/re-login."

    def test_e2e_single_product_purchase(self, logged_in_page):
        """E2E-001: Verify complete end-to-end flow for single product."""
        inventory_page = logged_in_page
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_FLEECE_JACKET)
        assert inventory_page.get_cart_count() == 2

        cart_page = inventory_page.navigate_to_cart()
        assert cart_page.get_cart_item_count() == 2
        assert Products.SAUCE_LABS_BACKPACK in cart_page.get_cart_item_names()
        assert Products.SAUCE_LABS_FLEECE_JACKET in cart_page.get_cart_item_names()

        checkout_info_page = cart_page.click_checkout()
        assert checkout_info_page.get_current_url() == Urls.CHECKOUT_STEP_ONE_URL

        checkout_info_page.fill_your_information(
            CheckoutInfo.STANDARD_USER_INFO["first_name"],
            CheckoutInfo.STANDARD_USER_INFO["last_name"],
            CheckoutInfo.STANDARD_USER_INFO["zip_code"]
        )
        checkout_overview_page = checkout_info_page.click_continue()
        assert checkout_overview_page.get_current_url() == Urls.CHECKOUT_STEP_TWO_URL

        # Verify details on overview page
        items_on_overview = checkout_overview_page.get_item_details()
        assert len(items_on_overview) == 2

        assert items_on_overview[0]["name"] == Products.SAUCE_LABS_BACKPACK
        # assert items_on_overview[0]["quantity"] == 1
        assert items_on_overview[0]["price"] == 29.99

        assert items_on_overview[1]["name"] == Products.SAUCE_LABS_FLEECE_JACKET
        # assert items_on_overview[1]["quantity"] == 1
        assert items_on_overview[1]["price"] == 49.99

        item_total = checkout_overview_page.get_item_total()
        tax = checkout_overview_page.get_tax()
        total = checkout_overview_page.get_total()

        assert item_total == 29.99 + 49.99
        # assert abs(tax - 7.60) < 0.01  # Allow for small floating point discrepancies
        # assert abs(total - (29.99 + 49.99 + 15.99)) < 0.01

        checkout_complete_page = checkout_overview_page.click_finish()
        assert checkout_complete_page.get_current_url() == Urls.CHECKOUT_COMPLETE_URL
        assert checkout_complete_page.get_complete_header_text() == ExpectedMessages.THANK_YOU_MESSAGE
        assert checkout_complete_page.get_complete_text_message() == ExpectedMessages.ORDER_DISPATCH_MESSAGE
        assert inventory_page.get_cart_count() == 0  # Cart should be empty after purchase

    def test_add_and_remove_products_from_inventory_page(self, logged_in_page):
        """E2E-003: Verify add/remove from cart on Inventory Page."""
        inventory_page = logged_in_page

        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        assert inventory_page.get_cart_count() == 1
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BACKPACK) == "Remove"

        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BIKE_LIGHT)
        assert inventory_page.get_cart_count() == 2
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BIKE_LIGHT) == "Remove"

        inventory_page.remove_product_from_cart(Products.SAUCE_LABS_BACKPACK)
        assert inventory_page.get_cart_count() == 1
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BACKPACK) == "Add to cart"

        inventory_page.remove_product_from_cart(Products.SAUCE_LABS_BIKE_LIGHT)
        assert inventory_page.get_cart_count() == 0
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BIKE_LIGHT) == "Add to cart"

    def test_checkout_missing_first_name(self, logged_in_page):
        """E2E-008: Verify checkout cannot proceed with missing First Name."""
        inventory_page = logged_in_page
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        cart_page = inventory_page.navigate_to_cart()
        checkout_info_page = cart_page.click_checkout()

        checkout_info_page.fill_your_information(
            "",  # Missing first name
            CheckoutInfo.STANDARD_USER_INFO["last_name"],
            CheckoutInfo.STANDARD_USER_INFO["zip_code"]
        )
        checkout_info_page.click_continue()  # This will not return a new page object

        assert checkout_info_page.is_error_message_visible()
        assert checkout_info_page.get_error_message() == ExpectedMessages.ERROR_FIRST_NAME_REQUIRED
        assert checkout_info_page.get_current_url() == Urls.CHECKOUT_STEP_ONE_URL