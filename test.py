#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ get the state with cities
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/states")
    r_j = r.json()
    
    state_id = None
    for state_j in r_j:
        rs = requests.get("http://0.0.0.0:5050/api/v1/states/{}/cities".format(state_j.get('id')))
        rs_j = rs.json()
        if len(rs_j) != 0:
            state_id = state_j.get('id')
            break
    
    if state_id is None:
        print("State with cities not found")
    
    """ Fetch cities
    """
    r = requests.get("http://0.0.0.0:5050/api/v1/states/{}/cities".format(state_id))
    r_j = r.json()
    print(type(r_j))
    print(len(r_j))
    for city_j in r_j:
        if city_j.get('name') in ["Fremont", "San Francisco", "San Diego"]:
            print("OK")
        else:
            print("Missing: {}".format(city_j.get('name')))
        if city_j.get('id') is None:
            print("Missing ID for City: {}".format(city_j.get('name')))