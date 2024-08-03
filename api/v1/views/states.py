#!/usr/bin/python3
""" State view """
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_state():
    """ Retrieves the list of all State """
    stat_obj = storage.all(State)
    return jsonify([obj.to_dict() for obj in stat_obj.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object by state_id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """ Delete a State object by state_id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()

    response = jsonify({})
    response.status_code = 200
    return response


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """ Returns the new created State object """
    new_state = request.get_json
    if not new_state:
        abort(400, 'Not a JSON')
    if 'name' not in new_state:
        abort(400, 'Missing name')

    storage.new(new_state)
    storage.save()

    response = jsonify(new_state.to_dict())
    response.status_code = 201
    return response


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def upd_state(state_id):
    """ Returns the updated State object by state_id """

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    new_state = request.get_json 
    if not new_state:
        abort(400, 'Not a JSON')

    for key, value in new_state.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()

    response = jsonify(state.to_dict())
    response.status_code = 200
    return response
