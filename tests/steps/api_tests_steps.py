from behave import given, when, then
import concurrent.futures

@given('the exchange rate service is available')
def step_impl_exchange_service(context):
    res = context.api.get_docs()
    assert res.status_code == 200, f"No access to exchange service: {res.text}"

@given('I have an account with "{amount}" "{currency}"')
def step_impl_create_source_account(context, amount, currency):
    res = context.api.create_account(currency)
    assert res.status_code == 201, f"Error creating account: {res.text}"
    context.source_account_id = res.json()["id"]

    deposit = context.api.deposit_money(context.source_account_id, currency, amount)
    assert deposit.status_code == 200, f"Error depositing money: {deposit.text}"

    context.initial_source_balance = amount
    context.source_currency = currency

@given('another user has an account with deposited "{amount}" "{currency}"')
def step_impl_create_target_account(context, amount, currency):
    res = context.api.create_account(currency)
    assert res.status_code == 201, f"Error creating target account: {res.text}"
    context.target_account_id = res.json()["id"]

    deposit = context.api.deposit_money(context.target_account_id, currency, amount)
    assert deposit.status_code == 200, f"Error depositing money to target: {deposit.text}"

    context.initial_target_balance = amount
    context.target_currency = currency


@when('I transfer "{amount}" "{currency}" to the other account')
def step_impl_transfer(context, amount, currency):
    context.transfer_amount = amount
    context.response = context.api.transfer_money(
        context.source_account_id,
        context.target_account_id,
        currency,
        context.transfer_amount
    )

@when('I try to transfer "{amount}" "{currency}" to account id "{account_id}"')
def step_impl_transfer_invalid(context, amount, currency, account_id):
    context.response = context.api.transfer_money(
        context.source_account_id,
        account_id,
        currency,
        amount
    )

@when('I execute "{num}" transfers in parallel of "{amount}" "{currency}" each')
def step_impl_concurrent_transfers(context, num, amount, currency):
    context.transfer_amount = amount

    with concurrent.futures.ThreadPoolExecutor(max_workers=int(num)) as executor:
        futures = [
            executor.submit(
                context.api.transfer_money,
                context.source_account_id,
                context.target_account_id,
                currency,
                context.transfer_amount
            )
            for _ in range(int(num))
        ]
        context.transfer_responses = [f.result() for f in concurrent.futures.as_completed(futures)]


@then('my account balance should be "{expected_balance}" "{currency}"')
def step_impl_verify_source_balance(context, expected_balance, currency):
    res = context.api.get_account(context.source_account_id)
    balance = res.json()["balance"]
    assert balance == float(expected_balance), f"Expected source balance {expected_balance}, got {balance}"


@then('the other account balance should be "{expected_balance}" "{currency}"')
def step_impl_verify_target_balance(context, expected_balance, currency):
    res = context.api.get_account(context.target_account_id)
    balance = res.json()["balance"]
    assert balance == float(expected_balance), f"Expected target balance {expected_balance}, got {balance}"


@then('I should receive an error message containing "{message}"')
def step_impl_verify_error(context, message):
    error_message = context.response.json()["message"]
    assert message in error_message, f"Expected error message to contain '{message}', got '{error_message}'"


@then('I should receive a "{status_code}" status code')
def step_impl_verify_status_code(context, status_code):
    expected = int(status_code)
    actual = context.response.status_code
    assert actual == expected, f"Expected status code {expected}, got {actual}"

@then('my account balance should remain "{amount}" "{currency}"')
def step_impl_verify_unchanged_source(context, amount, currency):
    res = context.api.get_account(context.source_account_id)
    balance = res.json()["balance"]
    assert balance == float(amount), f"Expected source balance to remain {amount}, got {balance}"

@then('the other account balance should remain "{amount}" "{currency}"')
def step_impl_verify_unchanged_target(context, amount, currency):
    res = context.api.get_account(context.target_account_id)
    balance = res.json()["balance"]
    assert balance == float(amount), f"Expected target balance to remain {amount}, got {balance}"

@then('all transfers should be successful')
def step_impl_verify_all_transfers(context):
    assert all(r.status_code == 200 for r in context.transfer_responses), "Not all transfers were successful"

@then('the final balances on other account should be "{expected_balance}"')
def step_impl_verify_final_balances(context, expected_balance):
    res = context.api.get_account(context.target_account_id)
    balance = res.json()["balance"]
    assert balance == float(expected_balance), f"Expected target balance {expected_balance}, got {balance}"

@when('I withdraw "{amount}" "{currency}"')
def step_impl_withdraw(context, amount, currency):
    context.response = context.api.withdraw_money(
        context.source_account_id,
        currency,
        amount
    )

@when('I try to transfer "{amount}" "{currency}" to same account')
def step_impl_transfer_invalid(context, amount, currency):
    context.response = context.api.transfer_money(
        context.source_account_id,
        context.source_account_id,
        currency,
        amount
    )