#!/usr/bin/env python3

from flask import Flask
import os

app = Flask(__name__)

# Get the port from environment variables, default to 5000 if not set
port = os.getenv('PORT', 5000)

@app.route('/')
def home():
    return f"Server started in port {port}"

if __name__ == '__main__':
    print(f"Server started in port {port}", flush=True)
    app.run(host='0.0.0.0', port=port)

