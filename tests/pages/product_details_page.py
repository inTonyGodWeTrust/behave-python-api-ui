from selenium.webdriver.common.by import By


class ProductDetailsPage():
    PRODUCT_TITLE = (By.XPATH, '//div[@class="shop_product_description"]/h1')

    def __init__(self, driver):
        self.driver = driver

    def check_product_name(self, title):
        product_title = self.driver.title
        return title in product_title