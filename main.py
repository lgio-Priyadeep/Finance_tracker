# main.py
from app import services


def main():
    print("Welcome to the Financial Tracker App (Dummy Version)")
    # Call a dummy transaction addition function
    services.add_transaction(100.0, "Test Expense")


if __name__ == "__main__":
    main()
