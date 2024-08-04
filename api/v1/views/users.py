#!/usr/bin/python3
""" Amenity view """
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all users objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates an User"""
    user = request.get_json()
    if not user:
        abort(400, description="Not a JSON")
    if 'email' not in user:
        abort(400, "Missing email")
    if 'password' not in user:
        abort(400, 'Missing password')

    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def upd_user(user_id):
    """Updates a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_user = request.get_json()
    if not new_user:
        abort(400, description="Not a JSON")

    for key, value in new_user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
