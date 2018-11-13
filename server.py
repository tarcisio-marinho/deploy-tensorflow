from flask import Flask, redirect
from flask import render_template, url_for
import os
import time
import subprocess

app = Flask("Simple-Web-Server")

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return redirect(url_for("classification"), code=302)


@app.route('/wait')
def wait():
    time.sleep(2)
    return ''

@app.route('/classification', methods=['GET'])
def classification():
    return render_template('classification.html')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)