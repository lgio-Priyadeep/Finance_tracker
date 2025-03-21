import os
import sys
from datetime import date
import pytest

# Ensure the project root is in sys.path so that imports work correctly.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the functions to test
from app.services import (
    add_manual_transaction,
    capture_bank_transactions,
    add_bill,
    add_bank_account,
    analyze_spending,
    estimate_tax,
)
from db import connection_pool

def create_test_user():
    """
    Inserts a test user with id = 1 into the users table.
    Uses ON CONFLICT to avoid duplicate insertion if the user already exists.
    Adjust the SQL according to your users table schema.
    """
    conn = None
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (id, username, email, password_hash)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                RETURNING id;
                """,
                (1, "testuser", "test@example.com", "hashed_password")
            )
            result = cur.fetchone()
            user_id = result[0] if result else 1
        conn.commit()
        return user_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            connection_pool.putconn(conn)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """
    Fixture that runs once per module.
    It creates a test user and can optionally clear or reset tables.
    """
    create_test_user()
    # Optionally, clear relevant tables before running tests
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE transactions RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE bills RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE bank_accounts RESTART IDENTITY CASCADE;")
        conn.commit()
    finally:
        connection_pool.putconn(conn)
    yield
    # Teardown code: optionally clear test data after tests finish

def test_add_manual_transaction():
    txn_id = add_manual_transaction(1, 100.0, "Test Expense", "Food")
    assert txn_id is not None, "Transaction ID should be returned for a valid insert."

def test_capture_bank_transactions():
    bank_data = [
        {"amount": 50.0, "date": date(2025, 3, 17), "description": "Bank Txn 1", "category": "Utilities"},
        {"amount": 75.0, "date": date(2025, 3, 17), "description": "Bank Txn 2", "category": "Travel"},
    ]
    txn_ids = capture_bank_transactions(1, bank_data)
    assert isinstance(txn_ids, list), "Expected a list of transaction IDs."
    assert len(txn_ids) == 2, "Should insert two bank transactions."

def test_add_bill():
    bill_id = add_bill(1, 200.0, date(2025, 4, 1), "Electricity Bill", status="pending")
    assert bill_id is not None, "Bill ID should be returned for a valid bill insertion."

def test_add_bank_account():
    account_id = add_bank_account(1, "Test Bank", "XXXX-XXXX-XXXX", balance=1000.0)
    assert account_id is not None, "Bank account ID should be returned for a valid insert."

def test_analyze_spending():
    # Insert expense transactions
    add_manual_transaction(1, 100.0, "Food expense", "Food")
    add_manual_transaction(1, 150.0, "Travel expense", "Travel")
    result = analyze_spending(1)
    assert "total_spent" in result, "Result must include a total_spent key."
    assert "category_breakdown" in result, "Result must include a category_breakdown key."
    assert result["total_spent"] >= 250, "Total spent should be at least 250."

def test_estimate_tax():
    # Insert an income transaction for testing tax estimation
    add_manual_transaction(1, 1000.0, "Salary", "Income", txn_type="income")
    tax_info = estimate_tax(1, tax_rate=0.1)
    assert tax_info["total_income"] >= 1000.0, "Total income should reflect the inserted income."
    assert tax_info["estimated_tax"] >= 100.0, "Estimated tax should be correctly calculated."
