#!/usr/bin/python3
"""
states view
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """ returns state(s) """
    objs_list = []
    objs = storage.all('State').values()

    for obj in objs:
        objs_list.append(obj.to_dict())

    return jsonify(objs_list)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_by_id(state_id):
    """ returns state """
    obj = storage.get('State', state_id)
    if obj != None:
        return obj.to_dict()
    abort(404)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def del_state(state_id):
    """ removes state obj """
    obj = storage.get('State', state_id)
    if obj != None:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/states', strict_slashes=False, methods=['POST'])
def new_state():
    """ creates state obj """
    obj_data = request.get_json()
    if not obj_data:
        abort(400, 'Not a JSON')
    if 'name' not in obj_data:
        abort(400, 'Missing name')

    obj = State(name=obj_data['name'])
    storage.new(obj)
    storage.save()

    return obj.to_dict(), 201

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ updates state """
    obj_data = request.get_json()
    if not obj_data:
        abort(400, 'Not a JSON')
    obj = storage.get('State', state_id)
    ignore_keys = ["id", "created_at", "updated_at"]

    for key, val in obj_data.items():
        for i_key in ignore_keys:
            if key != i_key:
                setattr(obj, key, val)
    return jsonify(obj.to_dict()), 200
