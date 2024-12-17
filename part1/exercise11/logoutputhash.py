#!/usr/bin/env python3

# Import libraries.
import time
import string
import random
from flask import Flask, Response

randomstring = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) # 8 length randomly generated string.
app = Flask(__name__) # Initialize flask app.

def datehash(randomstring):
    # This function gets the date and a random string and prints it.
    with open("/usr/src/app/logs/date.txt", "r") as f:
        date = f.read()
    print(date + ": " + randomstring, flush=True)

@app.route('/status', methods=['GET'])
def get_status():
    # Endpoint to return the current status
    with open("/usr/src/app/logs/date.txt", "r") as f:
        date = f.read()
    with open("/usr/src/app/logs/pingpong.txt", "r") as f:
        pongcount = f.read()    
    response_text = date + ": " + randomstring + "\n" + "Pings / Pongs: " + str(pongcount)
    return Response(response_text, mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    while True:
        datehash(randomstring)
        time.sleep(5) # 5 seconds delay between executions.
