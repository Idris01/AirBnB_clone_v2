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


@app.route('/states', strict_slashes=False)
def states():
    """Return List of all states
    """
    all_states = storage.all(State)
    data = [dict(
        name=state.name,
        id=state.id
        ) for state in all_states.values()]

    data.sort(key=lambda x: x['name'])
    return render_template("9-states.html", states=data, is_states=True)


@app.route('/states/<id>', strict_slashes=False)
def state_id(id):
    """Get All cities for a Given State
    """

    state_with_id = [
            state for state in
            list(storage.all(State).values())
            if state.id == id]
    if state_with_id:
        state_with_id = state_with_id[0]
        data = {}
        data['name'] = state_with_id.name
        cities = [dict(
            id=city.id, name=city.name
            ) for city in state_with_id.cities]
        cities.sort(key=lambda x: x['name'])
        data['cities'] = cities
        data['id'] = state_with_id.id
        state_with_id = data

    return render_template(
            '9-states.html',
            state=state_with_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
