## Sample Test framework for saucedemo
- Sample automation test for saucedemo E2E test - Powered by the pytest engine.
- It's built on Python apply the POM design pattern to ensure our tests are readable, robust & easy to maintain.
- Key features: 
logging, reporting, support flexible configuration for env, browser, headless mode; 
auto capture screenshot on failure or on demand, allure report for detail, Using UV for env management,
auto setup and run test in one script, easy to integrate with CI/CD like Jenkins, gitHub actions,...
- TODO: parallel test run(pytest-xdist), Apply testrail id to push to TestRail automatically(trcli),...

- Including test:

### 1. Authentication tests:
 + AUTH-001: Verify standard user can successfully log in
 + AUTH-002/3: Verify problem/performance glitch user can log in
 + AUTH-004, AUTH-005, AUTH-006, AUTH-007, AUTH-008, AUTH-009:
  Verify various invalid login attempts result in correct error messages and stay on login page.

### 2. E2E tests:
 + E2E-001: Verify cart is persistent after logout/re-login
 + E2E-002: Verify complete end-to-end flow for purchasing 2 products
 + E2E-003: Verify add/remove from cart on Inventory Page
 + E2E-004: Verify checkout cannot proceed with missing First Name

## Setup and run test

The script run_test.bat will install required env: Python, UV, package needed and then execute all test automatically

```commandline
# To setup and run all test:
run_test.bat

# To run the only test "test_e2e_products_purchase_success"
run_test.bat -k test_e2e_products_purchase_success

# To run all e2e tests:
run_test.bat -k e2e

# To run authentication tests:
run_test.bat -k authentication
```

## Output
The test output in the project/framework root, including:
+ allure-results: allure result to generate more html report
+ logs: test run log files
+ screenshots: screenshot output on failure(automatic capture) or on demand
+ report.html: simple html report from pytest
+ test_results.xml: junit xml result, to mapping ID & integrate with Test Management system like Test Rail
