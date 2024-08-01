#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    A class named User that represents a user

    Attributes:
        email (string): The email of the user, can't be null
        password (string): The password of the user, can't be null
        first_name (string): The first name of the user, can be null
        last_name (string): The last name of the user, can be null
        places (relationship): The relationship to Place objects
    """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship("Place", backref="user", cascade="all, delete")
