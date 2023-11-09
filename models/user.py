#!/usr/bin/python3
"""The User class definition"""
from models.base_model import BaseModel


class User(BaseModel):
    """The User class representation

Attributes:
first_name (str): user first name
last_name (str): user last name
email (str): user email
password (str): user password
"""


first_name = ""
last_name = ""
email = ""
password = ""
