#!/usr/bin/python3
"""
cities view
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ returns all City by State """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    cities_all = []
    cities = storage.all("City").values()
    for city in cities:
        if city.state_id == state_id:
            cities_all.append(city.to_json())
    return jsonify(cities_all)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_by_id(city_id):
    """ returns city  """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    city = city.to_json()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """ removws city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    """ new_city """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    obj_data = request.get_json()
    if obj_data is None:
        abort(400, "Not a JSON")
    if 'name' not in obj_data:
        abort(400, "Missing name")
    city = City(**obj_data)
    city.state_id = state_id
    city.save()
    city = city.to_json()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ updates city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    obj_data = request.get_json()
    if obj_data is None:
        abort(400, "Not a JSON")
    for key, value in obj_data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            city.bm_update(key, value)
    city.save()
    city = city.to_json()
    return jsonify(city), 200
