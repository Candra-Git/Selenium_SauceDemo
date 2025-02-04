from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def add_to_cart_from_detail(driver):
    # Add to cart from detail product
    driver.find_element(By.XPATH, "//a[@id='item_4_title_link']").click()
    driver.find_element(By.ID, "add-to-cart").click()
    driver.find_element(By.ID, "back-to-products").click()

    driver.find_element(By.XPATH, "//a[@id='item_0_title_link']").click()
    driver.find_element(By.ID, "add-to-cart").click()
    driver.find_element(By.ID, "back-to-products").click()

    driver.find_element(By.XPATH, "//a[@id='item_1_title_link']").click()
    driver.find_element(By.ID, "add-to-cart").click()
    driver.find_element(By.ID, "back-to-products").click()

def add_to_cart_from_product_list(driver):
    # Add to cart from button list products
    driver.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()
    driver.find_element(By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)").click()

def go_to_cart(driver):
    # Navigate to shopping cart
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
    )
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
