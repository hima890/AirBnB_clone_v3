#!/usr/bin/python3
"""
This module sets up the Flask application and its configurations,
including error handling and CORS policies.
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import environ
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """
    Close the database connection at the end of the request or when the application shuts down.
    
    Parameters:
    - error: The error that triggered the teardown, if any.
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    Custom error handler for 404 errors.
    
    Parameters:
    - error: The error object provided by Flask.
    
    Returns:
    A JSON response indicating that the requested resource was not found.
    """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(
        host=host,
        port=port,
        threaded=True,
        debug=True)
