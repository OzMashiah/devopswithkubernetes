#!/usr/bin/env python3

# Import libraries.
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__) # Initialize flask app.

# PostgreSQL connection details
DB_HOST = "postgres-svc"
DB_PORT = "5432"
DB_NAME = "pingpong"
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
    cur = conn.cursor()

    # Create the counter table if it doesn't exist
    cur.execute("""
            CREATE TABLE IF NOT EXISTS counter (
                id SERIAL PRIMARY KEY,
                value INT NOT NULL
            );
        """)

    # Insert an initial value for the counter if it's empty
    cur.execute("SELECT COUNT(*) FROM counter;")
    if cur.fetchone()[0] == 0:
       cur.execute("INSERT INTO counter (value) VALUES (0);")

    conn.commit()
    cur.close()
    conn.close()

    print("Database and table initialized.")

@app.route('/pingpong', methods=['GET'])
def get_status():
    # Endpoint to return the pong number.
    initialize_db()
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT value FROM counter WHERE id = 1')
    count = cur.fetchone()[0]
    count += 1

    cur.execute('UPDATE counter SET value = %s WHERE id = 1', (count,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        'pong': count 
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)    
