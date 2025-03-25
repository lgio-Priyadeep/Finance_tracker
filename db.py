# db.py
import os
import psycopg2
from psycopg2 import pool
import urllib.parse
import environ

# Initialize environ and read .env from the project root.
env = environ.Env()
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
environ.Env.read_env(os.path.join(project_root, '.env'))

# Retrieve connection parameters from environment variables
raw_user = env('DB_USER')      # e.g., "postgres"
raw_password = env('DB_PASSWORD')
host = env('DB_HOST')          # e.g., "localhost"
db_name = env('DB_NAME')       # e.g., "financial_tracker_db"

# URL-encode credentials
user = urllib.parse.quote_plus(raw_user)
password = urllib.parse.quote_plus(raw_password)

DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db_name}"

try:
    connection_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)
    if connection_pool:
        print("Connection pool created successfully")
except Exception as e:
    print("Error while connecting to PostgreSQL", e)
    raise e
