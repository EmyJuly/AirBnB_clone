#!/usr/bin/python3
"""The Place class definition"""
from models.base_model import BaseModel


class Place(BaseModel):
    """place class representation

    Attributes:
    user_id (str): User id
    city_id (str): City id
    name (str): name of the place
    description (str): description of the place
    number_rooms (int): number of rooms present
    number_bathrooms (int): number of bathrooms present
    max_guest (int): Highest number of guests to accommodate the place
    price_by_night (int): charges by night of the place
    latitude (float): latitude of the place
    longitude (float): longitude of the place
    amenity_ids (list): list of Amenity ids
    """
    user_id = ""
    city_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
