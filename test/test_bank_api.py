# tests/test_bank_api.py
import pytest
from app.services import fetch_bank_transactions

def test_fetch_bank_transactions(mocker):
    dummy_data =  [
        {
            "amount": 50.0,
            "date": "2025-03-17",
            "description": "Dummy Transaction - Utilities",
            "category": "Utilities"
        },
        {
            "amount": 75.5,
            "date": "2025-03-18",
            "description": "Dummy Transaction - Groceries",
            "category": "Groceries"
        },
        {
            "amount": 120.0,
            "date": "2025-03-19",
            "description": "Dummy Transaction - Entertainment",
            "category": "Entertainment"
        }
    ]
    # Use mocker to patch the function
    mocker.patch('app.services.fetch_bank_transactions', return_value=dummy_data)
    result = fetch_bank_transactions()
    assert result == dummy_data, "The fetched bank transactions should match the dummy data"
