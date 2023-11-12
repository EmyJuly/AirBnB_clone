#!/usr/bin/python3
"""Unittests for models/amenity.py

Unittest classes:
TestAmenity_save
TestAmenity_instantiation
TestAmenity_to_dict
"""

import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.amenity import Amenity


class TestAmenity_save(unittest.TestCase):
    """The unittests testing the save method of class Amenity"""

    @classmethod
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
        amen = Amenity()
        sleep(0.05)
        first_updated_at = amen.updated_at
        amen.save()
        self.assertLess(first_updated_at, amen.updated_at)

    def test_double_saves(self):
        amen = Amenity()
        sleep(0.05)
        first_updated_at = amen.updated_at
        amen.save()
        second_updated_at = amen.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amen.save()
        self.assertLess(second_updated_at, amen.updated_at)

    def test_save_with_arg(self):
        amen = Amenity()
        with self.assertRaises(TypeError):
            amen.save(None)

    def test_save_updates_file(self):
        amen = Amenity()
        amen.save()
        amenid = "Amenity." + amen.id
        with open("file.json", "r") as f:
            self.assertIn(amenid, f.read())


class TestAmenity_instantiation(unittest.TestCase):
    """The unittests testing instantiation of Amenity class"""

    def test_no_arguments_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_the_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_the_id_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_the_created_at_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_the_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amen = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amen.__dict__)

    def test_two_unique_amenities_ids(self):
        amen1 = Amenity()
        amen2 = Amenity()
        self.assertNotEqual(amen1.id, amen2.id)

    def test_two_different_amenities_created_at(self):
        amen1 = Amenity()
        sleep(0.05)
        amen2 = Amenity()
        self.assertLess(amen1.created_at, amen2.created_at)

    def test_two_different_amenities_updated_at(self):
        amen1 = Amenity()
        sleep(0.05)
        amen2 = Amenity()
        self.assertLess(amen1.updated_at, amen2.updated_at)

    def test_string_representation(self):
        now = datetime.now()
        now_repr = repr(now)
        amen = Amenity()
        amen.id = "123456"
        amen.created_at = amen.updated_at = now
        amenstr = amen.__str__()
        self.assertIn("[Amenity] (123456)", amenstr)
        self.assertIn("'id': '123456'", amenstr)
        self.assertIn("'created_at': " + now_repr, amenstr)
        self.assertIn("'updated_at': " + now_repr, amenstr)

    def test_unused_args(self):
        amen = Amenity(None)
        self.assertNotIn(None, amen.__dict__.values())

    def test_kwargs_instatiation(self):
        now = datetime.now()
        now_iso = now.isoformat()
        amen = Amenity(id="345", created_at=now_iso, updated_at=now_iso)
        self.assertEqual(amen.id, "345")
        self.assertEqual(amen.created_at, now)
        self.assertEqual(amen.updated_at, now)

    def test_instantiation_without_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_to_dict(unittest.TestCase):
    """The unittests testing the method to_dict in class Amenity"""

    def test_of_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_has_right_keys(self):
        amen = Amenity()
        self.assertIn("id", amen.to_dict())
        self.assertIn("created_at", amen.to_dict())
        self.assertIn("updated_at", amen.to_dict())
        self.assertIn("__class__", amen.to_dict())

    def test_to_dict_has_added_attributes(self):
        amen = Amenity()
        amen.middle_name = "Holberton"
        amen.my_number = 98
        self.assertEqual("Holberton", amen.middle_name)
        self.assertIn("my_number", amen.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        amen = Amenity()
        amen_dict = amen.to_dict()
        self.assertEqual(str, type(amen_dict["id"]))
        self.assertEqual(str, type(amen_dict["created_at"]))
        self.assertEqual(str, type(amen_dict["updated_at"]))

    def test_to_dict_output(self):
        now = datetime.now()
        amen = Amenity()
        amen.id = "123456"
        amen.created_at = amen.updated_at = now
        tdict = {
                'id': '123456',
                '__class__': 'Amenity',
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
                }
        self.assertDictEqual(amen.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        amen = Amenity()
        self.assertNotEqual(amen.to_dict(), amen.__dict__)

    def test_to_dict_using_arg(self):
        amen = Amenity()
        with self.assertRaises(TypeError):
            amen.to_dict(None)


if __name__ == "__main__":
    unittest.main()
