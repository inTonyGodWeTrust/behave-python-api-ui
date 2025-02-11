from behave import *

@given('open "{page}"')
def open_page(context, page):
    context.home_page.open_page(page)

@when('I navigate to the category within Products')
def navigate_products(context):
    context.home_page.hover_on_element(context.home_page.PRODUCTS_MENU)
    context.home_page.navigate_random(context.home_page.PRODUCT_DROPDOWN_LIST)

@when('I check that the number of the displayed products is greater than 0')
def products_greater_than_zero(context):
    assert context.product_page.list_of_products_greater_than_zero(), "no products on product page"

@when('I check that each product has a title and description')
def products_have_descr(context):
    assert context.product_page.all_products_have_info(), "Not all the products have title or text"

@when("Click on Read more button")
def click_on_readme(context):
    context.product_name = context.product_page.get_product_name()

@then('Check that you’re navigated to a product details page')
def open_product_detail(context):
    product_name = context.product_name
    assert context.product_details_page.check_product_name(product_name), "Product detail page title is incorrect."

