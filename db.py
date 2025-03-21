import os
import psycopg2
from psycopg2 import pool
import urllib.parse

# Retrieve connection parameters (adjust environment variables as needed)
raw_user = os.getenv("DB_USER", "postgres")
raw_password = os.getenv("DB_PASSWORD", "5568Post54673289*^gre")
host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "financial_tracker_db")

# URL-encode credentials to safely handle special characters
user = urllib.parse.quote_plus(raw_user)
password = urllib.parse.quote_plus(raw_password)

DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db_name}"

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)
    if connection_pool:
        print("Connection pool created successfully")
except Exception as e:
    print("Error while connecting to PostgreSQL", e)
