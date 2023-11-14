#!/usr/bin/python3
"""Unittests for models/base_model.py

Unittest classes:
TestBaseModel_save
TestBaseModel_instantiation
TestBaseModel_to_dict
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel_save(unittest.TestCase):
    """The unittests testing the save method"""
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_double_saves(self):
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bm.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_updates_file(self):
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModel_instantiation(unittest.TestCase):
    """The unittests testing instantiation of BaseModel class"""

    def test_no_arguments_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_the_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_the_id_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_the_created_at_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_the_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_with_unique_ids(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_different_created_at_models(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_different_updated_at_models(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_string_representation(self):
        now = datetime.now()
        now_repr = repr(now)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = now
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + now_repr, bmstr)
        self.assertIn("'updated_at': " + now_repr, bmstr)

    def test_unused_args(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_kwargs_instantiation(self):
        now = datetime.now()
        now_iso = now.isoformat()
        bm = BaseModel(id="345", created_at=now_iso, updated_at=now_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, now)
        self.assertEqual(bm.updated_at, now)

    def test_instantiation_without_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_args_and_kwargs_instantiation(self):
        now = datetime.now()
        now_iso = now.isoformat()
        bm = BaseModel("12", id="345", created_at=now_iso, updated_at=now_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, now)
        self.assertEqual(bm.updated_at, now)


class TestBaseModel_to_dict(unittest.TestCase):
    """The unittests testing the method to_dict"""

    def test_of_to_dict_type(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_has_right_keys(self):
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_has_added_attributes(self):
        bm = BaseModel()
        bm.name = "Holberton"
        bm.my_number = 98
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        now = datetime.now()
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = now
        tdict = {
                'id': '123456',
                '__class__': 'BaseModel',
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
                }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_using_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
