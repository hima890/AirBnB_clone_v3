#!/usr/bin/python3

from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = '421a55f4-7d82-47d9-b54c-a76916479546'
print("First state: {}".format(storage.get(State, first_state_id)))
