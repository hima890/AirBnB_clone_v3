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
        """Deserialize the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                objs = json.load(f)
                for key, obj_dict in objs.items():
                    class_name = obj_dict['__class__']
                    if 'id' not in obj_dict:
                        print("Missing 'id' key in {}".format(obj_dict))
                        continue
                    obj = globals()[class_name].from_dict(obj_dict)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass
        except KeyError as e:
            print("KeyError: {} in object {}".format(
                e,
                obj_dict
            ))

    def delete(self, key):
        """Deletes an object from __objects using its key and updates the
        JSON file."""
        if key in self.__objects:  # Directly access __objects
            print("Deleting {}".format(key))
            del self.__objects[key]  # Delete directly from __objects
            self.save()  # Ensure this method correctly updates the JSON file
        else:
            print("Key {} not found.".format(key))

    def get(self, cls, id):
        """Retrieves an object from the storage database by class and id."""
        if cls is not None and id is not None:
            objects = self.all(cls)
            for obj_id, obj in objects.items():
                if obj_id.split('.')[1] == id:
                    return obj
        return None

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class"""
        if cls:
            return len([
                obj for obj in self.all().values()
                if isinstance(obj, cls)
            ])
        return len(self.all())

    def close(self):
        """Close method for deserializing the JSON file to objects"""
        self.reload()
