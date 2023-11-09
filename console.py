#!/usr/bin/python3
"""Defines the HBnB console."""
import re
import cmd
from models.base_model import BaseModel
from models import storage
from shlex import split
from models.user import User
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.place import Place
from models.city import City
from models.review import Review
from models.amenity import Amenity
