#!/usr/bin/python3
"""Flask routes file logic"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''Returns the status of the API'''
    return jsonify({
        "status": "OK"
        })
