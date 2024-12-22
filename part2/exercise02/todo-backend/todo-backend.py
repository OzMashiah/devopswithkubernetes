from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for to-dos (will persist across restarts)
todos = []

# GET /todos - Retrieve all to-dos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# POST /todos - Create a new to-do
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo_item = data.get('todo')
    if todo_item:
        todos.append({'todo': todo_item})
        return jsonify({'message': 'Todo created successfully'}), 201
    else:
        return jsonify({'error': 'Todo item is required'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Running on port 5001
