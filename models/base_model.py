#!/usr/bin/python3
"""
This module contains the BaseModel class.
"""
from datetime import datetime
import uuid
import models
import os
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base


stroge_type = os.getenv('HBNB_TYPE_STORAGE')

if stroge_type == "db":
    Base = declarative_base()
else:
    Base = object

stroge_type = os.getenv('HBNB_TYPE_STORAGE')


class BaseModel:
    """
    This class serves as a base model for other classes.
    It provides attributes and methods common to all models.
    """
    if stroge_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DATETIME, default=datetime.utcnow)
        updated_at = Column(DATETIME, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.
        Attributes:
            id (str): A unique identifier generated using UUID.
            created_at (str): A string representation of the
            creation timestamp.
            updated_at (str): A string representation of the
            last update timestamp.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

            if "created_at" in kwargs.keys():
                self.created_at = datetime.strptime(
                    kwargs["created_at"], '%Y-%m-%dT%H:%M:%S.%f'
                )
            else:
                self.created_at = datetime.now()

            if "updated_at" in kwargs.keys():
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"], '%Y-%m-%dT%H:%M:%S.%f'
                )
            else:
                self.updated_at = datetime.now()

            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())

    @classmethod
    def from_dict(cls, obj_dict):
        """
        Recreates an instance of BaseModel from a dictionary representation.

        Args:
            obj_dict (dict): Dictionary representing the object.

        Returns:
            BaseModel: An instance of BaseModel.
        """
        # Assuming 'id', 'created_at', and 'updated_at' are present in obj_dict
        return cls(id=obj_dict['id'],
                   created_at=obj_dict['created_at'],
                   updated_at=obj_dict['updated_at'])

    def save(self):
        """
        Updates the 'updated_at' attribute with the current timestamp.
        """
        self.updated_at = datetime.now()
        # If it's a new instance, add it to the storage
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        res = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    res[key] = value.isoformat()
                else:
                    res[key] = value
        res['__class__'] = self.__class__.__name__
        return res

    def delete(self):
        """Deletes this BaseModel instance from the storage"""
        models.storage.delete(self)

    def __str__(self):
        """
        Returns a string representation of the object.
        Returns:
            str: A string containing the class name,
            ID, and attributes.
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
            )
