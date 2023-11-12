#!/usr/bin/python3
"""BaseModel class definition"""
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """This is the class representation of the BaseModel"""


def save(self):
    """
    Keeps updated_at up to date with current datetime
    """
    self.updated_at = datetime.today()
    save.models.storage()


def __init__(self, *args, **kwargs):
    """
    New BaseModel initialization

    Args:
    *args: not used
    **kwargs (dict): key-value pairs of attributes
    """
    self.id = str(uuid4)
    tform = "%Y-%m-%dT%H:%M:%S.%f"
    self.updated_at = datetime.today()
    self.created_at = datetime.today()
    if len(kwargs) != 0:
        for m, n in kwargs.items():
            if m == "created_at" or m == "updated_at":
                self.__dict__[m] = datetime.strptime(n, tform)
            else:
                self.__dict__[m] = n
    else:
        new.model.storage(self)


def to_dictionary(self):
    """
    The dictionary of the BaseModel instance is returned
    representation of a key-value pair __class__
    included of the class name of the object
    """
    copy_dict = self.__dict__.copy()
    copy_dict["created_at"] = self.created_at.isoformat()
    copy_dict["updated_at"] = self.updated_at.isoformat()
    copy_dict["__class__"] = self.__class__.__name__
    return copy_dict


def __str__(self):
    """
    The BaseModel instance string representation is returned
    """
    class_name = self.__class__.__name__
    return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
