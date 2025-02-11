import requests
from requests.exceptions import RequestException
from global_scope import *

class APIError(Exception):
    pass

class APIHelper:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def _make_request(self, method, endpoint, data=None):
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, json=data)
            return response
        except RequestException as e:
            raise APIError(f"API request failed: {str(e)}") from e

    def create_account(self, currency: str, account: str = ACCOUNT):
        return self._make_request("POST", account, {"currency": str(currency)})

    def deposit_money(self, account_id: int, currency: str, amount: float, deposit: str = TRANSACTION_DEPOSIT):
        data = {
            "accountId": account_id,
            "currency": currency,
            "amount": amount
        }
        return self._make_request("POST", deposit, data)

    def withdraw_money(self, account_id: int, currency: str, amount: float, withdraw: str = TRANSACTION_WITHDRAW):
        data = {
            "accountId": account_id,
            "currency": currency,
            "amount": amount
        }
        return self._make_request("POST", withdraw, data)

    def transfer_money(self, debit_account_id: int, credit_account_id: int, currency: str, amount: float, transfer: str = TRANSACTION_TRANSFER):
        data = {
            "debitAccountId": debit_account_id,
            "creditAccountId": credit_account_id,
            "currency": currency,
            "amount": amount
        }
        return self._make_request("POST", transfer, data)

    def get_account(self, account_id: int, account: str = ACCOUNT):
        return self._make_request("GET", f"{account}/{account_id}")

    def get_docs(self, documentation: str = DOCUMENTATION):
        return self._make_request("GET", documentation)