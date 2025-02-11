Feature: Fund Transfer API

  Background:
    Given the exchange rate service is available
  @api
  Scenario: Successful money transfer between accounts with same currency
    Given I have an account with "1000.00" "EUR"
    And another user has an account with deposited "500.00" "EUR"
    When I transfer "100.00" "EUR" to the other account
    Then my account balance should be "900.00" "EUR"
    And the other account balance should be "600.00" "EUR"

  @api
  Scenario Outline: Transfer money with currency exchange
    Given I have an account with "<from_amount>" "<from_currency>"
    And another user has an account with deposited "<to_initial>" "<to_currency>"
    When I transfer "<transfer_amount>" "<from_currency>" to the other account
    Then my account balance should be "<final_from>" "<from_currency>"
    And the other account balance should be "<increased_to>" "<to_currency>"

    Examples:
      | from_amount | from_currency  | to_initial | to_currency | transfer_amount | final_from | increased_to |
      | 1000.00     | EUR            | 500.00     | USD         | 100.00          | 900.00     |  608.6       |
      | 1000.00     | USD            | 500.00     | GBP         | 100.00          | 900.00     |  577.42      |

  @api
  Scenario: Transfer with insufficient funds
    Given I have an account with "100.00" "EUR"
    And another user has an account with deposited "500.00" "EUR"
    When I transfer "150.00" "EUR" to the other account
    Then I should receive an error message containing "insufficient balance"
    And my account balance should remain "100.00" "EUR"
    And the other account balance should remain "500.00" "EUR"

  @api
  Scenario: Transfer to non-existent account
    Given I have an account with "1000.00" "EUR"
    When I try to transfer "100.00" "EUR" to account id "123123123"
    Then I should receive a "404" status code
    And my account balance should remain "1000.00" "EUR"

  @api
  Scenario: Concurrent transfers between accounts
    Given I have an account with "1000.00" "EUR"
    And another user has an account with deposited "1000.00" "USD"
    When I execute "5" transfers in parallel of "100.00" "EUR" each
    Then all transfers should be successful
    And my account balance should be "500.00" "EUR"
    And the final balances on other account should be "1543.0"

  @api
  Scenario Outline: Withdraw with exact amount
    Given I have an account with "<from_amount>" "<from_currency>"
    When I withdraw "<withdraw_amount>" "<to_currency>"
    Then my account balance should be "<final_from>" "<from_currency>"
    Examples:
      | from_amount | from_currency   | to_currency | withdraw_amount | final_from |
      | 200.00    | EUR               | EUR         | 199.99          | 0.01       |
      | 200.00    | EUR               | USD         | 100.00          | 107.92     |

  @api
  Scenario: Send money to myself
    Given I have an account with "1000.00" "EUR"
    When I try to transfer "200.00" "EUR" to same account
    Then I should receive a "400" status code
    Then I should receive an error message containing "Transferring money from and to the same account is not allowed"
    And my account balance should remain "1000.00" "EUR"

  @api
  Scenario: Transfer should fail when exchange rate cannot be retrieved
    Given I have an account with "100" "EUR"
    And another user has an account with deposited "10" "GBP"
    When I transfer "5" "NIS" to the other account
    Then I should receive a "400" status code
    And I should receive an error message containing "invalid value"
    And my account balance should remain "100" "EUR"
    And the other account balance should remain "10" "GBP"