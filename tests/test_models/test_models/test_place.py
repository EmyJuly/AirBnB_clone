 #!/usr/bin/python3
"""The definition of unittests for models/place.py
Unittest classes: TestPlace_save TestPlace_instantiation TestPlace_to_dict
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime from models.place import Place
class TestPlace_save(unittest.TestCase):
"""The unittests testing the save method of class Place"""
@classmethod
def setUp(self):
try:
os.rename("file.json", "tmp") except IOError:
pass
def tearDown(self): try: os.remove("file.json") except IOError:
pass
try:
os.rename("tmp", "file.json") except IOError:
pass
def test_single_save(self):
env = Place()
sleep(0.05)
first_updated_at = env.updated_at
env.save()
self.assertLess(first_updated_at, env.updated_at)

 def test_double_saves(self):
env = Place()
sleep(0.05)
first_updated_at = env.updated_at env.save()
second_updated_at = env.updated_at self.assertLess(first_updated_at, second_updated_at) sleep(0.05)
env.save()
self.assertLess(second_updated_at, env.updated_at)
def test_save_with_arg(self):
env = Place()
with self.assertRaises(TypeError): env.save(None)
def test_save_updates_file(self): env = Place()
env.save()
envid = "Place." + env.id
with open("file.json", "r") as f: self.assertIn(envid, f.read())
class TestPlace_instantiation(unittest.TestCase): """The unittests testing instantiation of Place class"""
def test_no_arguments_instantiates(self): self.assertEqual(Place, type(Place()))
def test_the_new_instance_stored_in_objects(self): self.assertIn(Place(), models.storage.all().values())
def test_the_id_public_str(self): self.assertEqual(str, type(Place().id))
def test_the_created_at_public_datetime(self): self.assertEqual(datetime, type(Place().created_at))
def test_the_updated_at_public_datetime(self):

 self.assertEqual(datetime, type(Place().updated_at))
def test_city_id_is_public_class_attribute(self): env = Place()
self.assertEqual(str, type(Place.city_id)) self.assertIn("city_id", dir(env)) self.assertNotIn("city_id", env.__dict__)
def test_user_id_is_public_class_attribute(self): env = Place()
self.assertEqual(str, type(Place.user_id)) self.assertIn("user_id", dir(env)) self.assertNotIn("user_id", env.__dict__)
def test_name_is_public_class_attribute(self): env = Place()
self.assertEqual(str, type(Place.name)) self.assertIn("name", dir(env)) self.assertNotIn("name", env.__dict__)
def test_public_class_attribute_description(self): env = Place()
self.assertEqual(str, type(Place.description)) self.assertIn("description", dir(env)) self.assertNotIn("description", env.__dict__)
def test_the_number_of_rooms_is_public_class_attribute(self): env = Place()
self.assertEqual(int, type(Place.number_rooms) self.assertIn("number_rooms", dir(env)) self.assertNotIn("number_rooms", env.__dict__)
def test_the_number_of_bathrooms_is_public_class_attribute(self): env = Place()
self.assertEqual(int, type(Place.number_bathrooms)) self.assertIn("number_bathrooms", dir(env)) self.assertNotIn("number_bathrooms", env.__dict__)

 def test_the_max_guest_is_public_class_attribute(self): env = Place()
self.assertEqual(int, type(Place.max_guest)) self.assertIn("max_guest", dir(env)) self.assertNotIn("max_guest", env.__dict__)
def test_the_price_by_night_is_public_class_attribute(self): env = Place()
self.assertEqual(int, type(Place.price_by_night)) self.assertIn("price_by_night", dir(env)) self.assertNotIn("price_by_night", env.__dict__)
def test_the_latitude_is_public_class_attribute(self): env = Place()
self.assertEqual(float, type(Place.latitude)) self.assertIn("latitude", dir(env)) self.assertNotIn("latitude", env.__dict__)
def test_the_longitude_is_public_class_attribute(self): env = Place()
self.assertEqual(float, type(Place.longitude)) self.assertIn("longitude", dir(env)) self.assertNotIn("longitude", env.__dict__)
def test_the_amenity_ids_is_public_class_attribute(self): env = Place()
self.assertEqual(list, type(Place.amenity_ids)) self.assertIn("amenity_ids", dir(env)) self.assertNotIn("amenity_ids", env.__dict__)
def test_the_two_unique_places_ids(self): env1 = Place()
env2 = Place() self.assertNotEqual(env1.id, env2.id)
def test_the_two_different_places_created_at(self): env1 = Place()

 sleep(0.05)
env2 = Place()
self.assertLess(env1.created_at, env2.created_at)
def test_the_two_different_places_updated_at(self): env1 = Place()
sleep(0.05)
env2 = Place()
self.assertLess(env1.updated_at, env2.updated_at)
def test_string_representation(self): now = datetime.now()
now_repr = repr(now)
env = Place()
env.id = "123456"
env.created_at = env.updated_at = now
envstr = env.__str__()
self.assertIn("[Place] (123456)", envstr) self.assertIn("'id': '123456'", envstr) self.assertIn("'created_at': " + now_repr, envstr) self.assertIn("'updated_at': " + now_repr, envstr)
def test_unused_args(self):
env = Place(None)
self.assertNotIn(None, env.__dict__.values())
def test_kwargs_instatiation(self):
now = datetime.now()
now_iso = now.isoformat()
env = Place(id="345", created_at=now_iso, updated_at=now_iso) self.assertEqual(env.id, "345")
self.assertEqual(env.created_at, now) self.assertEqual(env.updated_at, now)
def test_instantiation_without_kwargs(self):
with self.assertRaises(TypeError):
Place(id=None, created_at=None, updated_at=None)

 class TestPlace_to_dict(unittest.TestCase):
"""The unittests testing the method to_dict in class Place"""
def test_of_to_dict_type(self): self.assertTrue(dict, type(Place().to_dict()))
def test_to_dict_has_right_keys(self): env = Place()
self.assertIn("id", env.to_dict()) self.assertIn("created_at", env.to_dict()) self.assertIn("updated_at", env.to_dict()) self.assertIn("__class__", env.to_dict())
def test_to_dict_has_added_attributes(self): env = Place()
env.middle_name = "Holberton" env.my_number = 98 self.assertEqual("Holberton", env.middle_name) self.assertIn("my_number", env.to_dict())
def test_to_dict_datetime_attributes_are_strings(self): env = Place()
env_dict = env.to_dict()
self.assertEqual(str, type(env_dict["id"])) self.assertEqual(str, type(env_dict["created_at"])) self.assertEqual(str, type(env_dict["updated_at"]))
def test_to_dict_output(self):
now = datetime.now()
env = Place()
env.id = "123456"
env.created_at = env.updated_at = now tdict = {
'id': '123456',
'__class__': 'Place',
'created_at': now.isoformat(), 'updated_at': now.isoformat()
}
self.assertDictEqual(env.to_dict(), tdict)

 def test_contrast_to_dict_dunder_dict(self): env = Place()
self.assertNotEqual(env.to_dict(), env.__dict__)
def test_to_dict_using_arg(self): env = Place()
with self.assertRaises(TypeError): env.to_dict(None)
if __name__ == "__main__": unittest.main()
