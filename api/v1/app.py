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
def not_found(error):
    """ Handler for 404 errors that returns a JSON-formatted response """
    return jsonify({
        "error": "Not found"
        }), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host,
            port=port,
            threaded=True)
