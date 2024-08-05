#!/usr/bin/python3
""" Amenity view """
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenities objects"""
    amenities = storage.all(Amenity)
    return jsonify([state.to_dict() for state in amenities.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(amenity_id):
    """Deletes a Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates an Amenity"""
    amenity = request.get_json()
    if not amenity:
        abort(400, description="Not a JSON")
    if 'name' not in amenity:
        abort(400, description="Missing name")

    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def upd_state(amenity_id):
    """Updates a Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, description="Not a JSON")

    for key, value in new_amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
