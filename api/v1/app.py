#!/usr/bin/python3
"""Flask server (variable app)"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def downtear(self):
    '''Closes storage on teardown'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''Handles 404 errors'''
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host,
            port=port,
            threaded=True,
            debug=True)
