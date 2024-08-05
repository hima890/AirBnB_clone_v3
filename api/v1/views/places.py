#!/usr/bin/python3
""" Amenity view """
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_Places(city_id):
    """Retrieves the list of all places objects"""
    places = storage.get(City, city_id)
    if not places:
        abort(404)
    return jsonify([place.to_dict() for place in places.values()])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Places object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates an Place"""
    city = request.get_json(City, city_id)
    if not city:
        abort(404)

    place = request.get_json()
    if not place:
        abort(400, description="Not a JSON")
    if 'user_id' not in place:
        abort(400, "Missing user_id")

    user_id = place['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in place:
        abort(400, "Missing name")

    new_place = Place(**place)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def upd_place(place_id):
    """Updates a Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    new_place = request.get_json()
    if not new_place:
        abort(400, description="Not a JSON")

    for key, value in new_place.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
