#!/usr/bin/python3
"""The unittests for city.py

Unittest classes:
    TestCity_save
    TestCity_instantiation
    TestCity_to_dict
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.city import City


class TestCity_save(unittest.TestCase):
    """The unittests testing the save method of class City"""

    @ classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_single_save(self):
        cty = City()
        sleep(0.05)
        first_updated_at = cty.updated_at
        cty.save()
        self.assertLess(first_updated_at, cty.updated_at)

    def test_double_saves(self):
        cty = City()
        sleep(0.05)
        first_updated_at = cty.updated_at
        cty.save()
        second_updated_at = cty.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cty.save()
        self.assertLess(second_updated_at, cty.updated_at)

    def test_save_with_arg(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.save(None)

    def test_save_updates_file(self):
        cty = City()
        cty.save()
        ctyid = "City." + cty.id
        with open("file.json", "r") as f:
            self.assertIn(ctyid, f.read())


class TestCity_instantiation(unittest.TestCase):
    """The unittests testing instantiation of City class"""

    def test_no_arguments_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_the_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_the_id_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_the_created_at_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_the_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_the_state_id_is_public_class_attribute(self):
        cty = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cty))
        self.assertNotIn("state_id", cty.__dict__)

    def test_name_is_public_class_attribute(self):
        cty = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(City()))
        self.assertNotIn("name", cty.__dict__)

    def test_two_unique_cities_ids(self):
        cty1 = City()
        cty2 = City()
        self.assertNotEqual(cty1.id, cty2.id)

    def test_two_different_cities_created_at(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.created_at, cty2.created_at)

    def test_two_different_cities_updated_at(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.updated_at, cty2.updated_at)

    def test_string_representation(self):
        now = datetime.now()
        now_repr = repr(now)
        cty = City()
        cty.id = "123456"
        cty.created_at = cty.updated_at = now
        ctystr = cty.__str__()
        self.assertIn("[City] (123456)", ctystr)
        self.assertIn("'id': '123456'", ctystr)
        self.assertIn("'created_at': " + now_repr, ctystr)
        self.assertIn("'updated_at': " + now_repr, ctystr)

    def test_unused_args(self):
        cty = City(None)
        self.assertNotIn(None, cty.__dict__.values())

    def test_kwargs_instatiation(self):
        now = datetime.now()
        now_iso = now.isoformat()
        cty = City(id="345", created_at=now_iso, updated_at=now_iso)
        self.assertEqual(cty.id, "345")
        self.assertEqual(cty.created_at, now)
        self.assertEqual(cty.updated_at, now)

    def test_instantiation_without_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class City_to_dict(unittest.TestCase):
    """The unittests testing the method to_dict in class City"""

    def test_of_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_has_right_keys(self):
        cty = City()
        self.assertIn("id", cty.to_dict())
        self.assertIn("created_at", cty.to_dict())
        self.assertIn("updated_at", cty.to_dict())
        self.assertIn("__class__", cty.to_dict())

    def test_to_dict_has_added_attributes(self):
        cty = City()
        cty.middle_name = "Holberton"
        cty.my_number = 98
        self.assertEqual("Holberton", cty.middle_name)
        self.assertIn("my_number", cty.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        cty = City()
        cty_dict = cty.to_dict()
        self.assertEqual(str, type(cty_dict["id"]))
        self.assertEqual(str, type(cty_dict["created_at"]))
        self.assertEqual(str, type(cty_dict["updated_at"]))

    def test_to_dict_output(self):
        now = datetime.now()
        cty = City()
        cty.id = "123456"
        cty.created_at = cty.updated_at = now
        tdict = {
                'id': '123456',
                '__class__': 'City',
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
                }
        self.assertDictEqual(cty.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        cty = City()
        self.assertNotEqual(cty.to_dict(), cty.__dict__)

    def test_to_dict_using_arg(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.to_dict(None)


if __name__ == "__main__":
    unittest.main()
