# init_db.py
from db import connection_pool


def initialize_database(sql_file="schema.sql"):
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            with open(sql_file, "r") as f:
                sql_script = f.read()
            cur.execute(sql_script)
        conn.commit()
        print("Database initialized successfully!")
    except Exception as e:
        conn.rollback()
        print("Error initializing database:", e)
    finally:
        connection_pool.putconn(conn)


if __name__ == "__main__":
    initialize_database()
