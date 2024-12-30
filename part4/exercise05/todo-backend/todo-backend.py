from flask import Flask, request, jsonify
import psycopg2
import os
import logging

app = Flask(__name__)

# Set up logging for request logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

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
            todo TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        );
        """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database and table initialized.")

@app.before_request
def log_request():
    logger.info(f"Request received: {request.method} {request.path}, Body: {request.get_data(as_text=True)}")

# GET / for health checks
@app.route('/', methods=['GET'])
def healthcheck():
    return 'OK', 200

# GET /todos - Retrieve all to-dos
@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, todo, done FROM todos")  # Include the 'done' status in the query
    todos = cursor.fetchall()
    todo_list = [{"id": todo[0], "todo": todo[1], "done": todo[2]} for todo in todos]

    cursor.close()
    conn.close()

    return jsonify(todo_list)

# POST /todos - Create a new to-do
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo_item = data.get('todo')

    if not todo_item:
        return jsonify({'error': 'To-do content is required'}), 400

    if len(todo_item) > 140:
        return jsonify({'error': 'To-do content exceeds 140 characters'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (todo) VALUES (%s) RETURNING id;", (todo_item,))
    new_id = cursor.fetchone()[0]
    conn.commit()  # Ensure the change is committed
    cursor.close()
    conn.close()

    return jsonify({'message': 'Todo created successfully', 'id': new_id}), 201

# healthz endpoint for readiness probe
@app.route('/healthz', methods=['GET'])
def readiness_check():
    try:
        conn = get_db_connection()
        conn.close()
        return 'Database connection is healthy', 200
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        return 'Database connection is unhealthy', 500

# PUT /todos/<id> - Update a to-do's done status
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo_status(id):
    data = request.get_json()
    done_status = data.get('done')  # This should be a boolean value

    if done_status is None:
        return jsonify({'error': 'Done status is required'}), 400

    # Validate that done_status is a boolean
    if not isinstance(done_status, bool):
        return jsonify({'error': 'Done status must be a boolean'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the done status of the to-do with the given id
    cursor.execute("""
        UPDATE todos
        SET done = %s
        WHERE id = %s
        RETURNING id, todo, done;
    """, (done_status, id))

    updated_todo = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if updated_todo:
        return jsonify({
            'message': 'To-do updated successfully',
            'id': updated_todo[0],
            'todo': updated_todo[1],
            'done': updated_todo[2]
        }), 200
    else:
        return jsonify({'error': 'To-do not found'}), 404

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5001)  # Running on port 5001
