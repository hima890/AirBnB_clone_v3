#!/usr/bin/python3
"""Cities API routes."""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False
                 )
def get_cities(state_id):
    """Retrieve the list of all City objects of a State"""
    state = storage.get(City, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a City"""
    state = storage.get(City, state_id)
    if not state:
        abort(404)
    # Try to get JSON data from the request
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    data = request.get_json()
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_city(state_id):
    """
    Updates a State object
    """
    state = storage.get(City, state_id)
    if not state:
        abort(404)

    # Try to get JSON data from the request
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    # Check if 'name' is in the JSON data
    if 'city' not in data:
        abort(400, description="Missing name")

    # Update the State object
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
