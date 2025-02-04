import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from test_saucedemo.list_Products import add_to_cart_from_detail, add_to_cart_from_product_list, go_to_cart
from test_saucedemo.test_users import users
from test_saucedemo.conftest import take_screenshot


@pytest.mark.parametrize("user", users, ids=[user["username"] for user in users])
def test_login(driver, user):
    driver.find_element(By.ID, "user-name").send_keys(user["username"])
    driver.find_element(By.ID, "password").send_keys(user["password"])

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
    take_screenshot(driver, f"login_{user['username']}")

    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inventory_container")))
    take_screenshot(driver, f"dashboard_{user['username']}")

    # Assertion: make sure user can login
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", "Login fail! URL not match."
    assert driver.find_element(By.ID, "inventory_container").is_displayed(), "Dashboard page not appear!"

def test_products(driver, login):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inventory_container")))
    take_screenshot(driver, "products_list")

    add_to_cart_from_detail(driver)
    add_to_cart_from_product_list(driver)

    go_to_cart(driver)
    take_screenshot(driver, "cart_after_add")

    assert driver.current_url == "https://www.saucedemo.com/cart.html", "Fail add cart!"
    assert driver.find_element(By.CLASS_NAME, "cart_item").is_displayed(), "cart is empty!"

def test_cart(driver, login, cart):
    """checking menu cart (remove product & checkout)."""
    remove_button = driver.find_element(By.ID, "remove-test.allthethings()-t-shirt-(red)")
    assert remove_button.is_displayed(), "Button remove not exist!"

    remove_button.click()
    driver.find_element(By.ID, "continue-shopping").click()

    assert driver.current_url == "https://www.saucedemo.com/inventory.html", "Failed to return to the product list!"

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    take_screenshot(driver, "cart_checkout")

    assert driver.current_url == "https://www.saucedemo.com/checkout-step-one.html", "failed to checkout!"

def test_information(driver, checkout):
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    postal_code = fake.zipcode()

    driver.find_element(By.ID, "first-name").send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    driver.find_element(By.ID, "continue").click()
    take_screenshot(driver, "checkout_information")

    assert driver.current_url == "https://www.saucedemo.com/checkout-step-two.html", "Failed to enter the checkout overview page!"

def test_overview(driver, checkout, info):
    finish_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "finish")))
    assert finish_button.is_displayed(), "Button 'Finish' not appear!"

    finish_button.click()
    take_screenshot(driver, "checkout_overview")

    success_message = driver.find_element(By.CLASS_NAME, "complete-header")
    assert success_message.is_displayed(), "success message not appear!"
    assert "Thank you for your order!" in success_message.text, "Checkout failed, confirmation text doesn't match!"
