#!/usr/bin/env python3

# Import libraries.
import time
import datetime
import string
import random 
from flask import Flask, Response
import requests
import os

randomstring = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) # 8 length randomly generated string.
app = Flask(__name__) # Initialize flask app.

@app.route('/', methods=['GET'])
def get_status():
    # Endpoint to return the current status (timestamp and random string)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = requests.get("http://pingpong-svc:2345/pingpong").json().get('pong')
    message_env = os.environ['MESSAGE']
    with open('/config/information.txt', 'r') as f:
        content = f.read()
        responsemessage = f"file content: {content}env variable: MESSAGE={message_env}\n{date}: {randomstring}.\nPing / Pongs: {count}" 
    return Response(responsemessage, mimetype='text/plain')

@app.route('/healthz', methods=['GET'])
def readiness_probe():
    try:
        response = requests.get("http://pingpong-svc:2345/pingpong", timeout=5)
        response.raise_for_status()
        return 'Backend is healthy and reachable', 200
    except requests.exceptions.RequestException as e:
        print(f"Backend connection error: {e}")
        return 'Backend is unhealthy or unreachable', 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)    
