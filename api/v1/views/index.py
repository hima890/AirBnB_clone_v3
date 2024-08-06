#!/usr/bin/python3
"""Flask routes file logic"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''Returns the status of the API'''
    if request.method == 'GET':
        return jsonify({
            "status": "OK"
            })


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returns the number of each object by type"""
    stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(stats)
