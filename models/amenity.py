#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel

if os.getenv('HBNB_TYPE_STORAGE') != 'db':

    class Amenity(BaseModel):
        """Define Amenity Class for file storage
        """
        name = ""
else:
    from sqlalchemy import Column, Integer, String
    from models.base_model import Base
    from models.place import place_amenity
    from sqlalchemy.orm import relationship

    class Amenity(BaseModel, Base):
        """Define Amenity class For db storage
        """
        __tablename__ = 'amenities'

        name = Column(String(128), nullable=False)
        place_amenities = relationship(
                "Place",
                secondary=place_amenity,
                back_populates="amenities")
