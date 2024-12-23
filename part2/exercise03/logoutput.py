#!/usr/bin/env python3

# Import libraries.
import time
import datetime
import string
import random 
from flask import Flask, Response
import requests

randomstring = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) # 8 length randomly generated string.
app = Flask(__name__) # Initialize flask app.

@app.route('/status', methods=['GET'])
def get_status():
    # Endpoint to return the current status (timestamp and random string)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = requests.get("http://pingpong-svc:2345/pingpong").json().get('pong')
    responsemessage = f"{date}: {randomstring}.\nPing / Pongs: {count}" 
    return Response(responsemessage, mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)    