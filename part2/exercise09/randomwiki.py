import requests
import psycopg2
import os

# PostgreSQL connection details
DB_HOST = "postgres-svc"
DB_PORT = "5432"
DB_NAME = "todo"
DB_USER = "postgres"
DB_PASSWORD = os.environ['DB_PASSWORD']

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def initialize_db():
    conn = psycopg2.connect(
            dbname='postgres',  # Default database to connect to (required to create other databases)
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    conn.autocommit = True
    cur = conn.cursor()

    # create database if does not exists
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database '{DB_NAME}' created.")

    conn.close()

    conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    cursor = conn.cursor()

    # Create the counter table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            todo TEXT NOT NULL
        );
        """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database and table initialized.")

def create_todo():
    r = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    todo_item = "Read "+ r.url
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (todo) VALUES (%s) RETURNING id;", (todo_item,))
    new_id = cursor.fetchone()[0]
    conn.commit() 
    cursor.close()
    conn.close()

if __name__ == '__main__':
    initialize_db()
    create_todo()
