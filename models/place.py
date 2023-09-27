#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    import sqlalchemy
    from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
    from models.base_model import Base
    from sqlalchemy.orm import relationship

    place_amenity = Table(
            'place_amenity', Base.metadata,
            Column(
                'place_id', String(60), ForeignKey('places.id'),
                primary_key=True, nullable=False),
            Column(
                'amenity_id', String(60), ForeignKey('amenities.id'),
                primary_key=True, nullable=False))

    class Place(BaseModel, Base):
        """ A place to stay """
        __tablename__ = 'places'

        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")

        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship(
                "Amenity", secondary=place_amenity,
                viewonly=False)


else:

    class Place(BaseModel):
        """ A place to stay """

        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter property that returns list of Review instances that
            show the relationship between Place and Review"""
            from models import storage
            rev_list = []
            all_revs = storage.all(Review)
            for review in all_revs.values():
                if review.place_id == self.id:
                    rev_list.append(review)
            return rev_list
