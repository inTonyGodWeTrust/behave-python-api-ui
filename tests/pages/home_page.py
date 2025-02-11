from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import random

class HomePage():
    PRODUCTS_MENU = (By.XPATH, '//a[@name="Products"]')
    PRODUCT_DROPDOWN_LIST = (By.XPATH, '//li[a[@name="Products"]]/ul/li/a/span[@class="main_title"]')

    def __init__(self, driver):
        self.driver = driver

    def open_page(self, page):
            self.driver.get(page)
            self.driver.add_cookie({
                'name': 'SystemCookieChoiceDecision',
                'value': '1=30'
            })
            self.driver.refresh()

    def hover_on_element(self, locator):
        action = ActionChains(self.driver)
        element = self.driver.find_element(*locator)
        action.move_to_element(element).perform()

    def navigate_random(self, locator):
        category_elements = self.driver.find_elements(*locator)
        random_category = random.choice(category_elements)
        random_category.click()