#!/usr/bin/python3
"""
states view
"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage

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
