#!/usr/bin/python3
""" Index view """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API in JSON """
    return jsonify({"status": "OK"})
