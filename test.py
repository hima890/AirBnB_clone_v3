#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    city_id = "nop"

    """ PUT /api/v1/cities/<city_id>
    """
    r = requests.put("http://0.0.0.0:5050/api/v1/cities/{}".format(city_id), data=json.dumps({ 'name': "NewName" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)