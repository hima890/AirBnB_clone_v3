#!/usr/bin/python3
"""
class named review that inharits from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Represent a review

    Attributes:
        place_id (string): The Place id
        user_id (string): The User id
        text (string): The text of the review

    """
    __tablename__ = 'reviews'

    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)
