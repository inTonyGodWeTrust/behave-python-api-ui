from selenium.webdriver.common.by import By
import random

class ProductPage():
    PRODUCT_TITLE = (By.XPATH, '//strong[@class="name"]')
    PRODUCT_TEXT = (By.XPATH, '//p[@class="teaser"]')
    READ_MORE_BUTTON = (By.XPATH, '//a[@class="viewproduct"]')
    LIST_OF_PRODUCTS = (By.XPATH, '(//div[@class="shop_productlistdynamiccolumns"]/div)')

    def __init__(self, driver):
        self.driver = driver

    def get_product_name(self):
        product_elements = self.driver.find_elements(*self.LIST_OF_PRODUCTS)
        random_product = random.choice(product_elements)
        product_name = random_product.find_element(*self.PRODUCT_TITLE).text
        random_product.find_element(*self.READ_MORE_BUTTON).click()
        return product_name

    def list_of_products_greater_than_zero(self):
        list_of_products = self.driver.find_elements(*self.LIST_OF_PRODUCTS)
        return len(list_of_products) > 0

    def all_products_have_info(self) -> bool:
        products = self.driver.find_elements(*self.LIST_OF_PRODUCTS)

        return all(
            product.find_element(*self.PRODUCT_TITLE).is_displayed() and
            product.find_element(*self.PRODUCT_TEXT).is_displayed()
            for product in products
        )