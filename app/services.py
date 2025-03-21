from decimal import Decimal
from datetime import datetime
from db import connection_pool

def create_test_user():
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            # Adjust the columns as per your users table definition.
            cur.execute(
                """
                INSERT INTO users (id, username, email, password_hash)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (1, "testuser", "test@example.com", "hashed_password")
            )
            user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection_pool.putconn(conn)



def add_manual_transaction(user_id, amount, description, category, txn_date=None, txn_type="expense", source="cash"):
    conn = None
    txn_date = txn_date or datetime.utcnow().date()
    query = """
        INSERT INTO transactions (user_id, amount, date, description, category, type, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    params = (user_id, amount, txn_date, description,
              category, txn_type.lower(), source)
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(query, params)
            txn_id = cur.fetchone()[0]
        conn.commit()
        return txn_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            connection_pool.putconn(conn)


def capture_bank_transactions(user_id, bank_data):
    """
    Inserts multiple bank transactions.
    bank_data: a list of dictionaries with keys: amount, date, description, category.
    """
    conn = None
    query = """
        INSERT INTO transactions (user_id, amount, date, description, category, type, source)
        VALUES (%s, %s, %s, %s, %s, 'expense', 'bank')
        RETURNING id;
    """
    txn_ids = []
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            for record in bank_data:
                params = (
                    user_id,
                    record.get("amount"),
                    record.get("date"),
                    record.get("description"),
                    record.get("category"),
                )
                cur.execute(query, params)
                txn_ids.append(cur.fetchone()[0])
        conn.commit()
        return txn_ids
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            connection_pool.putconn(conn)


def add_bill(user_id, amount, due_date, description, status="pending"):
    """
    Inserts a bill record into the bills table.
    Assumes a table with columns: id, user_id, amount, due_date, description, status.
    """
    conn = None
    query = """
        INSERT INTO bills (user_id, amount, due_date, description, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """
    params = (user_id, amount, due_date, description, status)
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(query, params)
            bill_id = cur.fetchone()[0]
        conn.commit()
        return bill_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            connection_pool.putconn(conn)


def add_bank_account(user_id, bank_name, account_number, balance=0.0):
    """
    Inserts a bank account record into the bank_accounts table.
    Assumes columns: id, user_id, bank_name, account_number, balance.
    """
    conn = None
    query = """
        INSERT INTO bank_accounts (user_id, bank_name, account_number, balance)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    params = (user_id, bank_name, account_number, balance)
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(query, params)
            account_id = cur.fetchone()[0]
        conn.commit()
        return account_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            connection_pool.putconn(conn)


def analyze_spending(user_id):
    """
    Analyzes spending for a user.
    Returns a dictionary with total spent and breakdown by category.
    """
    conn = None
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            query = """
                SELECT category, SUM(amount) AS total
                FROM transactions
                WHERE user_id = %s AND type = 'expense'
                GROUP BY category;
            """
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            total_spent = sum(row[1] for row in rows)
            category_breakdown = {
                row[0] or "Uncategorized": row[1] for row in rows}
        return {"total_spent": total_spent, "category_breakdown": category_breakdown}
    finally:
        if conn:
            connection_pool.putconn(conn)


def estimate_tax(user_id, tax_rate=0.10):
    """
    Calculates estimated tax for a user based on income transactions.
    Assumes income transactions have type 'income'.
    """
    conn = None
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            query = """
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE user_id = %s AND type = 'income';
            """
            cur.execute(query, (user_id,))
            total_income = cur.fetchone()[0]
            # Convert tax_rate to Decimal to multiply with total_income
            estimated_tax = total_income * Decimal(str(tax_rate))
        return {"total_income": total_income, "estimated_tax": estimated_tax}
    finally:
        if conn:
            connection_pool.putconn(conn)

# app/services.py

def fetch_bank_transactions():
    """
    Dummy implementation of fetching bank transactions.
    
    In production, this function would connect to a bank API,
    authenticate, and fetch transactions, parsing the returned data
    into a standardized format.
    
    For now, this function returns a fixed set of dummy transaction data.
    """
    dummy_transactions = [
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
    return dummy_transactions

