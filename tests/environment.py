from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.home_page import HomePage
from pages.product_details_page import ProductDetailsPage
from pages.product_page import ProductPage
from api_helper import APIHelper
import os


def before_scenario(context, scenario):
    if "api" not in scenario.effective_tags:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')

        if os.environ.get('DOCKER_ENV'):
            chrome_options.add_argument('--disable-gpu')
            chrome_options.binary_location = '/usr/bin/chromium'
            chromedriver_path = '/usr/bin/chromedriver'
        else:
            chromedriver_path = None

        if chromedriver_path:
            service = Service(executable_path=chromedriver_path)
            context.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
        else:
            context.driver = webdriver.Chrome(options=chrome_options)

        context.driver.maximize_window()

        context.home_page = HomePage(context.driver)
        context.product_page = ProductPage(context.driver)
        context.product_details_page = ProductDetailsPage(context.driver)

    context.api = APIHelper()

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
        except Exception as e:
            print(f"Error closing WebDriver: {e}")