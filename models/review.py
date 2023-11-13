#!/usr/bin/python3
"""The Review class definition"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class represenation

    Attributes:
    place_id (str): place id
    user_id(str): user id
    text (str): review text
    """
    place_id = ""
    user_id = ""
    text = ""
