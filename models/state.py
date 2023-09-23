#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship

is_db = os.getenv("HBNB_TYPE_STORAGE") == 'db'

if is_db:
    from models.city import City

    class State(BaseModel, Base):
        """ State class """
        __tablename__ = 'states'

        name = Column(String(128), nullable=False)
        cities = relationship(
                'City', cascade='all, delete-orphan',
                backref='state')
else:
    from models import storage

    class State(BaseModel):
        name = ""

        @property
        def cities(self):
            """ A property that return list of all cities in database
            """
            values = []
            for key, item in storage.all().items():
                if "City" in key and item.state_id == self.id:
                    values.append(item)
            return values
