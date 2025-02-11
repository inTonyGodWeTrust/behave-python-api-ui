Feature: UI test coverage
@ui
  Scenario: Check product details page
    Given Open "https://gomspace.com/"
    When  I navigate to the category within Products
    When  I check that the number of the displayed products is greater than 0
    When  I check that each product has a title and description
    When  Click on Read more button
    Then  Check that you’re navigated to a product details page