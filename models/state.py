#!/usr/bin/python3
"""
class named state that inharits from BaseModel
"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City

stroge_type = os.getenv('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """A class named State that represents a state"""
    if stroge_type == "db":
        __tablename__ = 'states'

        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if stroge_type != "db":
        @property
        def cities(self):
            """
            Getter attribute that returns the list of City instances with
            state_id equals to the current State.id
            """
            from models import storage
            city_list = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
