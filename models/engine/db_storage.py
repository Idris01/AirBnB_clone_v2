#!/usr/bin/python3
"""DBStorage Module

This module define a new storage engine 'DBStorage
"""
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.place import Place
from models.base_model import Base


mysql_user = os.getenv("HBNB_MYSQL_USER")
mysql_user_pwd = os.getenv("HBNB_MYSQL_PWD")
mysql_host = os.getenv("HBNB_MYSQL_HOST")
mysql_db = os.getenv("HBNB_MYSQL_DB")
is_test_env = os.getenv("HBNB_ENV") == 'test'

cls_map = dict(
        User=User, State=State, City=City,
        Amenity=Amenity, Place=Place, Review=Review)


class DBStorage:
    """A Relational database storage engine
    """
    __engine = None
    __session = None

    def __init__(self):
        """ initialize the instance attributes of the class
        """
        self.__engine = create_engine(
                "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                    mysql_user, mysql_user_pwd, mysql_host, mysql_db),
                pool_pre_ping=True)
        if is_test_env:
            db = self.__engine.cursor()
            session = scoped_session(
                    sessionmaker(bind=self.__engine)
                    )()
            metadata = MetaData(bind=self.__engine)
            metadata.reflect()
            for table_name in metadata.tables.keys():
                session.execute(
                        'DROP TABLE IF EXISTS {} CASCADE;'.format(table_name))
            session.commit()
            session.close()

    def all(self, cls=None):
        """Query the database for all objects
        """
        all_objects = {}

        cls_name = cls.__name__ if cls is not None else cls

        if cls is not None and cls_name in cls_map:
            all_cls = self.__session.query(cls_map[cls_name]).all()
            for item in all_cls:
                item = item.to_dict()
                item.pop('__class__')
                item_id = item.get("id")
                all_objects[f"{cls_name}.{item_id}"] = item

        elif cls is None:
            for name, obj in cls_map.items():
                try:
                    all_cls = self.__session.query(obj)
                    for item in all_cls:
                        item = item.to_dict()
                        cls_name = item.pop('__class__')
                        item_id = item.get("id")
                        all_objects[f"{cls_name}.{item_id}"] = item
                except Exception:
                    pass

        to_return = []

        for key, value in all_objects.items():
            this_class, this_id = key.split(".")
            value["updated_at"] = datetime.fromisoformat(value["updated_at"])
            value["created_at"] = datetime.fromisoformat(value["created_at"])
            to_return.append(f"[{this_class}] ({this_id}) {value}")
        return to_return

    def new(self, cls):
        """Add new object to the current database
        """
        if type(cls).__name__ in cls_map:
            self.__session.add(cls)

    def save(self):
        """Commit all changes of the current database
        """

        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database
        """

        if obj and type(obj).__name__ in cls_map:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database

        Also creates the current database session
        """

        Base.metadata.create_all(self.__engine)

        factory_session = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False)
        self.__session = scoped_session(factory_session)

    def close(self):
        """Close the database
        """
        if self.__session is not None:
            self.__session.remove()
