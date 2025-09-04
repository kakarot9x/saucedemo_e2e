# tests/test_cart_persistence.py
import logging

from constants import Urls
from tests.data import Products, User, CheckoutInfo, ExpectedMessages
from pages.login_page import LoginPage

log = logging.getLogger(__name__)


class TestE2ECheckOut:
    def test_cart_state_after_logout_and_relogin(self, driver):
        """E2E-001: Verify cart is persistent after logout/re-login."""

        log.info("Step 1. Login to web with valid credential")
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        inventory_page = login_page.login(User.STANDARD_USER["username"], User.STANDARD_USER["password"])

        log.info("Step 2. Add 3 products to cart and check cart quantity")
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_ONESIE)
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BIKE_LIGHT)
        assert inventory_page.get_cart_count() == 3, "Incorrect products count on cart"

        log.info("Step 3. Logout and check if is on login page")
        inventory_page.logout()
        login_page.verify_on_login_page()

        log.info("Step 4. Re-login and check product are persistent on cart")
        inventory_page_after_relogin = login_page.login(User.STANDARD_USER["username"], User.STANDARD_USER["password"])
        assert inventory_page_after_relogin.get_cart_count() == 3, "Cart was cleared after logout/re-login."

    def test_e2e_products_purchase_success(self, logged_in_page):
        """E2E-002: Verify complete end-to-end flow for single product."""
        log.info("Step 1. Login to web with valid credential")
        inventory_page = logged_in_page

        log.info("Step 2. Adding 2 products to cart")
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_FLEECE_JACKET)
        assert inventory_page.get_cart_count() == 2, "Incorrect products count"

        log.info("Step 3. Navigate to cart detail and check products on cart")
        cart_page = inventory_page.navigate_to_cart()
        assert cart_page.get_cart_item_count() == 2, "Incorrect products count on cart"
        assert Products.SAUCE_LABS_BACKPACK in cart_page.get_cart_item_names(), \
            f"Selected product {Products.SAUCE_LABS_BACKPACK} not exist on cart"
        assert Products.SAUCE_LABS_FLEECE_JACKET in cart_page.get_cart_item_names(), \
            f"Selected product {Products.SAUCE_LABS_FLEECE_JACKET} not exist on cart"

        log.info("Step 4. Click checkout to navigate to checkout page")
        checkout_info_page = cart_page.click_checkout()
        assert checkout_info_page.get_current_url() == Urls.CHECKOUT_STEP_ONE_URL, "Incorrect Step 1 URL"

        log.info("Step 5. Fill delivery info and continue")
        checkout_info_page.fill_your_information(
            CheckoutInfo.STANDARD_USER_INFO["first_name"],
            CheckoutInfo.STANDARD_USER_INFO["last_name"],
            CheckoutInfo.STANDARD_USER_INFO["zip_code"]
        )
        checkout_overview_page = checkout_info_page.click_continue()
        assert checkout_overview_page.get_current_url() == Urls.CHECKOUT_STEP_TWO_URL, "Incorrect Step 2 URL"

        log.info("Step 6. Verify details on overview page")
        items_on_overview = checkout_overview_page.get_item_details()
        assert len(items_on_overview) == 2, "Incorrect items on overview page"

        assert items_on_overview[0]["name"] == Products.SAUCE_LABS_BACKPACK, "Incorrect first product"
        assert items_on_overview[0]["price"] == 29.99

        assert items_on_overview[1]["name"] == Products.SAUCE_LABS_FLEECE_JACKET, "Incorrect second product"
        assert items_on_overview[1]["price"] == 49.99

        log.info("Step 7. Verify total price with tax info")
        item_total = checkout_overview_page.get_item_total()
        tax = checkout_overview_page.get_tax()
        total = checkout_overview_page.get_total()
        assert item_total == 29.99 + 49.99
        log.info(f"Tax: {tax}, Total Price: {total}")

        log.info("Step 8. Verify check out success with correct url and thank you message")
        checkout_complete_page = checkout_overview_page.click_finish()
        assert checkout_complete_page.get_current_url() == Urls.CHECKOUT_COMPLETE_URL
        assert checkout_complete_page.get_complete_header_text() == ExpectedMessages.THANK_YOU_MESSAGE
        assert checkout_complete_page.get_complete_text_message() == ExpectedMessages.ORDER_DISPATCH_MESSAGE
        assert inventory_page.get_cart_count() == 0

    def test_add_and_remove_products_from_inventory_page(self, logged_in_page):
        """E2E-003: Verify add/remove from cart on Inventory Page."""

        log.info("Step 1. Login to web with valid credential")
        inventory_page = logged_in_page

        log.info("Step 2. Adding 1st product to cart, check remove button present")
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        assert inventory_page.get_cart_count() == 1
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BACKPACK) == "Remove"

        log.info("Step 3. Adding 2nd product to cart, check remove button present")
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BIKE_LIGHT)
        assert inventory_page.get_cart_count() == 2
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BIKE_LIGHT) == "Remove"

        log.info("Step 4. Remove 1st product from cart, check add button present")
        inventory_page.remove_product_from_cart(Products.SAUCE_LABS_BACKPACK)
        assert inventory_page.get_cart_count() == 1
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BACKPACK) == "Add to cart"

        log.info("Step 5. Remove 2nd product from cart, check add button present")
        inventory_page.remove_product_from_cart(Products.SAUCE_LABS_BIKE_LIGHT)
        assert inventory_page.get_cart_count() == 0
        assert inventory_page.get_product_button_text(Products.SAUCE_LABS_BIKE_LIGHT) == "Add to cart"

    def test_checkout_missing_first_name(self, logged_in_page):
        """E2E-004: Verify checkout cannot proceed with missing First Name."""

        log.info("Step 1. Login to web with valid credential")
        inventory_page = logged_in_page

        log.info("Step 2. Adding 1st product to cart and checkout")
        inventory_page.add_product_to_cart(Products.SAUCE_LABS_BACKPACK)
        cart_page = inventory_page.navigate_to_cart()
        checkout_info_page = cart_page.click_checkout()

        log.info("Step 3. Fill delivery info without First Name and click continue")
        checkout_info_page.fill_your_information(
            "",  # Empty first name
            CheckoutInfo.STANDARD_USER_INFO["last_name"],
            CheckoutInfo.STANDARD_USER_INFO["zip_code"]
        )
        checkout_info_page.click_continue()

        log.info("Step 4. Verify error message showing and staying Step 1 URL")
        assert checkout_info_page.is_error_message_visible()
        assert checkout_info_page.get_error_message() == ExpectedMessages.ERROR_FIRST_NAME_REQUIRED
        assert checkout_info_page.get_current_url() == Urls.CHECKOUT_STEP_ONE_URL