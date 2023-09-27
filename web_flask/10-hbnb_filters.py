#!/usr/bin/python3
"""Query All cities by state
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def refresh_storage(exception):
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Filter route of hbnb website
    """
    all_states = []
    states = list(storage.all(State).values())
    states.sort(key=lambda x: x.name)
    for state in states:
        data = {}
        data['name'] = state.name
        cities = [dict(
            id=city.id, name=city.name
            ) for city in state.cities]
        cities.sort(key=lambda x: x['name'])
        data['cities'] = cities
        data['id'] = state.id
        all_states.append(data)

    amenities = storage.all(Amenity).values()
    amenities = [amenity.name for amenity in amenities]
    amenities.sort()

    return render_template(
            "10-hbnb_filters.html",
            states=all_states,
            amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
