#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import os
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, DateTime

Base = declarative_base()

is_db = os.getenv("HBNB_TYPE_STORAGE") == 'db'


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            updated_at = kwargs.get('updated_at')
            if updated_at is not None:
                kwargs['updated_at'] = datetime.strptime(
                        updated_at, '%Y-%m-%dT%H:%M:%S.%f')

            created_at = kwargs.get('created_at')
            if created_at is not None:
                kwargs['created_at'] = datetime.strptime(
                        created_at, '%Y-%m-%dT%H:%M:%S.%f')

            if kwargs.get('__class__') is not None:
                del kwargs['__class__']

            self.__dict__.update(kwargs)
            if 'id' not in self.__dict__:
                self.id = str(uuid.uuid4())
            if 'created_at' not in self.__dict__:
                self.created_at = datetime.now()
            if 'updated_at' not in self.__dict__:
                self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        for i in self.__dict__:
            if '_sa_instance_state' in self.__dict__:
                del self.__dict__[i]
                break
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def __repr__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']

        return dictionary

    def delete(self):
        """Delete the instance from storage"""

        storage.delete(self)
