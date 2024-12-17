#!/usr/bin/env python3

# Import libraries.
from flask import Flask, jsonify

count = 0 # ping-pong counter.
app = Flask(__name__) # Initialize flask app.

@app.route('/pingpong', methods=['GET'])
def get_status():
    # Endpoint to return the pong number.
    global count 
    count += 1
    return jsonify({
        'pong': count 
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)    
