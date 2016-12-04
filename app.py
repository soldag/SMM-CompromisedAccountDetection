from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/check/')
def check():
    return render_template('check.html')
