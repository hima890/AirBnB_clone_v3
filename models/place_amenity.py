from sqlalchemy import Table, Column, String, ForeignKey
from models.base_model import Base
import os


stroge_type = os.getenv('HBNB_TYPE_STORAGE')

if stroge_type == 'db':
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
               "place_id",
               String(60),
               ForeignKey("places.id"),
               primary_key=True,
               nullable=False),
        Column(
               "amenity_id",
               String(60),
               ForeignKey("amenities.id"),
               primary_key=True,
               nullable=False)
    )
