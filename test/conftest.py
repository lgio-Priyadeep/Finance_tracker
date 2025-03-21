# tests/conftest.py
import os
import sys

# Determine the project root directory (one level up from the test folder)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Optional: Print out sys.path for debugging
print("Project root added to sys.path:", project_root)

from datetime import date
import pytest
from db import connection_pool  # Ensure project root is in PYTHONPATH (see below)

# Add the project root to sys.path if needed.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def create_test_user():
    """Ensure a test user with id = 1 exists."""
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (id, username, email, password_hash)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (1, "testuser", "test@example.com", "hashed_password")
            )
        conn.commit()
    finally:
        connection_pool.putconn(conn)

@pytest.fixture(scope="function", autouse=True)
def isolate_db():
    """
    This fixture runs before each test function.
    It resets the database state by truncating relevant tables.
    """
    # Set up: create test user and clear tables.
    create_test_user()
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
    # Optional: Teardown can go here if further cleanup is needed.
