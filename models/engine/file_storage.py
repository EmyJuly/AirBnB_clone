#!/usr/bin/python3
"""FileStorage class definition"""
import json
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.base_model import BaseModel


class FileStorage:
    """
    Abstract storage engine representation

    Attributes:
    __file_path (str): file name to save objects to
    __objects(dict): Instantiated objects dictionary
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        The dictionary __objects is returned
        """
        return FileStorage.__objects

    def save(self):
        """
        __objects serialization to JSON file __file_path
        """
        objdict = FileStorage.__objects
        newobjdict = {obj: objdict[obj].to_dict() for obj in objdict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(newobjdict, f)

    def new(self, obj):
        """
        __objects is set with <obj_class_name>.id key
        """
        objclname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(objclname, obj.id)] = obj

    def reload(self):
        """
        JSON file __file_path deserialized to __objects when it exists
        """
        try:
            with open(FileStorage.__file_path) as f:
                newobjdict = json.load(f)
                for o in newobjdict.values():
                    class_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
