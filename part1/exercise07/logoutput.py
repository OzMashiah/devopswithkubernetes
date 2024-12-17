#!/usr/bin/env python3

# Import libraries.
import time
import datetime
import string
import random 
from flask import Flask, jsonify

randomstring = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) # 8 length randomly generated string.
app = Flask(__name__) # Initialize flask app.

def datehash(randomstring):
    # This function gets the date and a random string and prints it.
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # current date formatted to string.
    print(date + ": " + randomstring, flush=True)

@app.route('/status', methods=['GET'])
def get_status():
    # Endpoint to return the current status (timestamp and random string)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        'timestamp': date,
        'random_string': randomstring
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)    
    while True:
        datehash(randomstring)
        time.sleep(5) # 5 seconds delay between executions.
