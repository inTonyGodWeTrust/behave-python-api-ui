import os

ACCOUNT = "/account"
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
DOCUMENTATION = "/v3/api-docs"
TRANSACTION_DEPOSIT = "/transaction/deposit"
TRANSACTION_WITHDRAW = "/transaction/withdraw"
TRANSACTION_TRANSFER = "/transaction/transfer"