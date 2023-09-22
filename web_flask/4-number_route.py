#!/usr/bin/python3
"""Hello Flask Module

Starts a flask web server on host 0.0.0.0 and port 5000
"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """Handles the default route
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """Handles the /hbnb route
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """Handles the path /c/<text> with a variable string 'text'
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/<text>', strict_slashes=False)
def python_route(text='is_cool'):
    """Handles the path /python/<text> with a variable string 'text'
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
def python_is_cool():
    """Handles the path /python with
    """
    return "Python is cool"


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """Handles the path /number/n with n being an integer
    """
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
