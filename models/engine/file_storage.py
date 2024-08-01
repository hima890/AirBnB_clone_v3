#!/usr/bin/python3
"""
This module contains the FileStorage class for managing
storage of models in a JSON file.
"""
# file_storage.py
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

import json


class FileStorage:
    """
        This class serializes instances to a JSON file and
        deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage.
        If cls is provided, returns only objects of that type."""
        if cls:
            return {k: v for k, v in self.__objects.items() if isinstance(
                v, cls)}
        return self.__objects

    def new(self, obj):

        """
        sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file
        """
        serialized_objs = {}
        for key, obj in self.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objs, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects if the file exists.
        If the file doesn't exist, do nothing.
        """
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, obj_dict in data.items():
                    class_name, obj_id = key.split('.')
                    obj = globals()[class_name].from_dict(obj_dict)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, key):
        """Deletes an object from __objects using its key and updates the
        JSON file."""
        objects = self.all()
        if key in objects:
            del objects[key]
            self.save()

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is None:
            return
        else:
            objects = self.all()
            # Use list to avoid RuntimeError during deletion
            for key, value in list(objects.items()):
                if value == obj:
                    del objects[key]
                    self.save()
                    # Exit loop after deleting the object
                    break
