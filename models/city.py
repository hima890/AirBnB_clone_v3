import os
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


stroge_type = os.getenv('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    if stroge_type == "db":
        __tablename__ = 'cities'

        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)

        # Ensure this backref is unique and does not conflict
        places = relationship("Place",
                              back_populates="city",
                              cascade="all, delete,delete-orphan")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
