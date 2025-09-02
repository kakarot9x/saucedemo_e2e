# saucedemo_e2e
Sample automation test for saucedemo E2E test - Powered by the pytest engine.
It's built on Python apply the POM design pattern to ensure our tests are readable, robust & easy to maintain.

Including test:
- Basic authentication with default listed users
- E2E Test:
 + adding to cart randomly 2 products
 + logout and login back to check that the products in the carts keep unchanged
 + process checkout: fill in detail information related to orders and delivery then checkout and validate that received success message
