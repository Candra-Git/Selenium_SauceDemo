import pytest
import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from test_saucedemo.list_Products import add_to_cart_from_detail, add_to_cart_from_product_list, go_to_cart



#for webdriver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

#for login to sauce demo
@pytest.fixture
def login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inventory_container")))


@pytest.fixture
def cart(driver, login):
    add_to_cart_from_detail(driver)
    add_to_cart_from_product_list(driver)
    go_to_cart(driver)

@pytest.fixture
def checkout(driver, login, cart):
    driver.find_element(By.ID, "remove-test.allthethings()-t-shirt-(red)").click()
    driver.find_element(By.ID, "continue-shopping").click()

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )

@pytest.fixture
def info(driver, checkout):
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    postal_code = fake.zipcode()

    driver.find_element(By.ID, "first-name").send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    driver.find_element(By.ID, "continue").click()

#Create a unique directory based on timestamp to store screenshots
timestamp = time.strftime("%Y%m%d-%H%M%S")
screenshot_dir = f"screenshots/{timestamp}"
os.makedirs(screenshot_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def take_screenshot(driver, name):
    filename = f"{screenshot_dir}/{name}.png"
    total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
    driver.set_window_size(driver.get_window_size()["width"], total_height)
    driver.save_screenshot(filename)
    logging.info(f"Screenshot saved: {filename}")
