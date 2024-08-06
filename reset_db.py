# reset_db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.place_amenity import place_amenity
import os

# Environment variables
user = os.getenv('HBNB_MYSQL_USER')
password = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
database = os.getenv('HBNB_MYSQL_DB')

# Create engine and bind it to the metadata
engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{database}')

# Drop all tables
Base.metadata.drop_all(engine)

print("All tables dropped.")
