#!/usr/bin/python3
"""
class named review that inharits from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
import os

stroge_type = os.getenv('HBNB_TYPE_STORAGE')


class Review(BaseModel, Base):
    """Represent a review

    Attributes:
        place_id (string): The Place id
        user_id (string): The User id
        text (string): The text of the review

    """
    if stroge_type == 'db':
        __tablename__ = 'reviews'

        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
