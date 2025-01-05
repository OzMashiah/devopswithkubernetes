from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def serve_content():
    # Read the website content from the file created from the ConfigMap
    with open('/usr/share/config/index.html', 'r') as file:
        website_content = file.read()
    return website_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
