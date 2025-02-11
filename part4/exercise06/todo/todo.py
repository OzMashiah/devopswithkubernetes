#!/usr/bin/env python3

from flask import Flask, send_from_directory, render_template, request, jsonify
import os
import time
import requests
import threading

app = Flask(__name__)

port = os.getenv('PORT', 5000)

BROADCASTER_URL = "http://broadcaster-svc:2345"

received_tasks = []

# Homepage route.
@app.route('/')
def home():
    return render_template("index.html", port=port)

# Image route.
@app.route('/image')
def serve_image():
    return send_from_directory("/usr/src/app/images/", 'picsum.jpg')

def download_image():
    while True:
        response = requests.get("https://picsum.photos/1200", allow_redirects=True)
        with open("/usr/src/app/images/picsum.jpg", "wb") as f:
            f.write(response.content)
        time.sleep(3600)  # Download every hour

@app.route('/healthz', methods=['GET'])
def readiness_probe():
    try:
        response = requests.get("http://todo-backend-svc:2345/todos", timeout=5)
        response.raise_for_status()
        return 'Backend is healthy and reachable', 200
    except requests.exceptions.RequestException as e:
        print(f"Backend connection error: {e}")
        return 'Backend is unhealthy or unreachable', 500

        return jsonify({"error": f"Error fetching tasks: {e}"}), 500

# Route to receive JSON data from the broadcaster (POST)
@app.route('/received-tasks', methods=['POST'])
def save_received_tasks():
    try:
        # Get JSON data from the request
        task_data = request.json
        received_tasks.append(task_data)  # Store it in memory
        print(received_tasks)
        print(f"Received task data: {task_data}")
        return jsonify({"message": "Task saved successfully"}), 200
    except Exception as e:
        print(f"Error saving task: {e}")
        return jsonify({"error": f"Error saving task: {e}"}), 500

# New route to view all saved tasks (GET)
@app.route('/received-tasks', methods=['GET'])
def show_received_tasks():
    return jsonify(received_tasks), 200

if __name__ == '__main__':
    # Start the image downloading in a separate thread
    download_thread = threading.Thread(target=download_image)
    download_thread.daemon = True  # Ensure the thread stops when the main program exits
    download_thread.start()

    app.run(host='0.0.0.0', port=port)
