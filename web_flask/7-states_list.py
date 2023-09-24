#!/usr/bin/python3
"""This module define a route that list all states
"""

from flask import Flask, render_template
import re
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def refresh_context(exception):
    """Delete context for each request
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Return List of all states
    """
    pattern = r"'name':\s'(?P<name>\w+)'.*?id':\s'(?P<id>[a-z-0-9]+)'"
    all_states = storage.all(State)
    data = [re.search(
        pattern, state).groupdict() for state in all_states]

    data.sort(key=lambda x: x['name'])
    return render_template("7-states_list.html", states=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
