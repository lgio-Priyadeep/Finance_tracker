from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import os

# Create the base class for our models
Base = declarative_base()

# Define enums for transaction types and bill status


class TransactionType(enum.Enum):
    expense = "expense"
    income = "income"


class BillStatus(enum.Enum):
    pending = "pending"
    paid = "paid"

# Define the User model


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    # Relationships to other tables
    transactions = relationship(
        "Transaction", back_populates="user", cascade="all, delete")
    bills = relationship("Bill", back_populates="user", cascade="all, delete")
    bank_accounts = relationship(
        "BankAccount", back_populates="user", cascade="all, delete")
    budgets = relationship(
        "Budget", back_populates="user", cascade="all, delete")

# Define the Transaction model (for both income and expenses)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    category = Column(String)
    type = Column(Enum(TransactionType), nullable=False)
    source = Column(String)  # e.g., "bank" or "cash"
    user = relationship("User", back_populates="transactions")

# Define the Bill model


class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(BillStatus), default=BillStatus.pending)
    description = Column(String)
    user = relationship("User", back_populates="bills")

# Define the BankAccount model


class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bank_name = Column(String, nullable=False)
    # Ideally, store masked data
    account_number = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    user = relationship("User", back_populates="bank_accounts")

# Define the Budget model


class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String, nullable=False)
    allocated_amount = Column(Float, nullable=False)
    spent_amount = Column(Float, default=0.0)
    user = relationship("User", back_populates="budgets")


# Database Initialization
if __name__ == "__main__":
    # You can set your PostgreSQL connection parameters via environment variables or directly here
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "5568Post54673289*^gre")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "financial_tracker_db")

    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(connection_string)

    # Create all tables in the database
    Base.metadata.create_all(engine)
    print("Database and tables created successfully!")
