#!/usr/bin/python3
""" Index view """
from api.v1.views import app_views
from flask import jsonify


@app_views.route(
    '/status',
    methods=['GET'],
    strict_slashes=False)
def status():
    """ Status of API in JSON """
    return jsonify({"status": "OK"})


@app_views.route(
    '/stats',
    methods=['GET'],
    strict_slashes=False)
def stats():
    """ Endpoint that retrieves the number of each objects by type """
    from models import storage
    from models.state import State
    from models.city import City
    from models.user import User
    from models.place import Place
    from models.amenity import Amenity
    from models.review import Review
    from models.state import State

    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)

    return jsonify(
        {
            "amenities": amenities,
            "cities": cities,
            "places": places,
            "reviews": reviews,
            "states": states,
            "users": users})
