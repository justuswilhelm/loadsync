"""
Get a continuous stream on the command-line:

curl -X get http://127.0.0.1:5000/large.csv

Same using requests:

import requests
r = requests.get('http://127.0.0.1:5000/large.csv', stream=True)
for line in r.iter_lines(chunk_size=16):
    print(line)
    if line: # filter out keep-alive new lines
        print(line)

r = requests.get('http://127.0.0.1:5000/large.csv', stream=True)
for line in r.iter_lines(chunk_size=1):
    print(line)

r = requests.get('http://127.0.0.1:5000/large.csv', stream=True)
for line in r.iter_content(chunk_size=16):
    print(line)

Tags: flask requests stream http mqtt
"""

import time
from datetime import datetime

from flask import Flask, Response


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello Stream!"


@app.route('/large.csv')
def generate_large_csv():
    "Generate and serve a continuous stream of timestamps."
    def generate():
        # while True:
        for i in range(10):
            time.sleep(0.1)
            yield datetime.now().isoformat() + '\n'
    return Response(generate(), mimetype='text/csv')


if __name__ == "__main__":
    app.run(debug=False)
