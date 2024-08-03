#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


"""A unique FileStorage/DBStorage instance for all models."""
stroge_type = os.getenv('HBNB_TYPE_STORAGE')
if stroge_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
