# data.py

class User:
 STANDARD_USER = {"username": "standard_user", "password": "secret_sauce"}
 LOCKED_OUT_USER = {"username": "locked_out_user", "password": "secret_sauce"}
 PROBLEM_USER = {"username": "problem_user", "password": "secret_sauce"}
 PERFORMANCE_GLITCH_USER = {"username": "performance_glitch_user", "password": "secret_sauce"}


class Products:
 SAUCE_LABS_BACKPACK = "Sauce Labs Backpack"
 SAUCE_LABS_BIKE_LIGHT = "Sauce Labs Bike Light"
 SAUCE_LABS_BOLT_T_SHIRT = "Sauce Labs Bolt T-Shirt"
 SAUCE_LABS_FLEECE_JACKET = "Sauce Labs Fleece Jacket"
 SAUCE_LABS_ONESIE = "Sauce Labs Onesie"
 ALL_THE_THINGS_T_SHIRT_RED = "Test.allTheThings() T-Shirt (Red)"


class ExpectedMessages:
 ERROR_USERNAME_REQUIRED = "Epic sadface: Username is required"
 ERROR_PASSWORD_REQUIRED = "Epic sadface: Password is required"
 ERROR_INVALID_CREDENTIALS = "Epic sadface: Username and password do not match any user in this service"
 ERROR_LOCKED_OUT_USER = "Epic sadface: Sorry, this user has been locked out."
 ERROR_FIRST_NAME_REQUIRED = "Error: First Name is required"
 ERROR_LAST_NAME_REQUIRED = "Error: Last Name is required"
 ERROR_POSTAL_CODE_REQUIRED = "Error: Postal Code is required"
 THANK_YOU_MESSAGE = "Thank you for your order!"
 ORDER_DISPATCH_MESSAGE = "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
 AUTH_ERROR_RESTRICTED_ACCESS = "Epic sadface: You can only access '{path}' when you are logged in."


class CheckoutInfo:
 STANDARD_USER_INFO = {"first_name": "John", "last_name": "Doe", "zip_code": "12345"}
 ANOTHER_USER_INFO = {"first_name": "Jane", "last_name": "Smith", "zip_code": "98765"}