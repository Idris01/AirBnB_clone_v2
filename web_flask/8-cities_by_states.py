#!/usr/bin/python3
"""Query All cities by state
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def refresh_storage(exception):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Get All cities for a Given State
    """
    states = list(storage.all(State).values())
    states.sort(key=lambda x: x.name)
    return render_template(
            '8-cities_by_states.html',
            states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
