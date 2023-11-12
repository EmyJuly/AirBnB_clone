#!/usr/bin/python3
"""
The unittests testing state.py

Unittest classes:
    TestState_save
    TestState_instantiation
    TestState_to_dict
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime from models.state import State


class TestState_save(unittest.TestCase):
    """The unittests testing the save method of class State"""

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
        ste = State()
        sleep(0.05)
        first_updated_at = ste.updated_at
        ste.save()
        self.assertLess(first_updated_at, ste.updated_at)

    def test_double_saves(self):
        ste = State()
        sleep(0.05)
        first_updated_at = ste.updated_at ste.save()
        second_updated_at = ste.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ste.save()
        self.assertLess(second_updated_at, ste.updated_at)

    def test_save_with_arg(self):
        ste = State()
        with self.assertRaises(TypeError):
            ste.save(None)

    def test_save_updates_file(self):
        ste = State()
        ste.save()
        steid = "State." + ste.id
        with open("file.json", "r") as f:
            self.assertIn(steid, f.read())


class TestState_instantiation(unittest.TestCase):
    """The unittests testing instantiation of State class"""

    def test_no_arguments_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_the_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_the_id_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_the_created_at_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_the_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        ste = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(ste))
        self.assertNotIn("name", ste.__dict__)

    def test_two_unique_states_ids(self):
        ste1 = State()
        ste2 = State()
        self.assertNotEqual(ste1.id, ste2.id)

    def test_two_different_states_created_at(self):
        ste1 = State()
        sleep(0.05)
        ste2 = State()
        self.assertLess(ste1.created_at, ste2.created_at)

    def test_two_different_states_updated_at(self):
        ste1 = State()
        sleep(0.05)
        ste2 = State()
        self.assertLess(ste1.updated_at, ste2.updated_at)

    def test_string_representation(self):
        now = datetime.now()
        now_repr = repr(now)
        ste = State()
        ste.id = "123456"
        ste.created_at = ste.updated_at = now
        stestr = ste.__str__()
        self.assertIn("[State] (123456)", stestr)
        self.assertIn("'id': '123456'", stestr)
        self.assertIn("'created_at': " + now_repr, stestr)
        self.assertIn("'updated_at': " + now_repr, stestr)

    def test_unused_args(self):
        ste = State(None)
        self.assertNotIn(None, ste.__dict__.values())

    def test_kwargs_instatiation(self):
        now = datetime.now()
        now_iso = now.isoformat()
        ste = State(id="345", created_at=now_iso, updated_at=now_iso)
        self.assertEqual(ste.id, "345")
        self.assertEqual(ste.created_at, now)
        self.assertEqual(ste.updated_at, now)

    def test_instantiation_without_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_to_dict(unittest.TestCase):
    """The unittests testing the method to_dict in class State"""

    def test_of_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_has_right_keys(self):
        ste = State()
        self.assertIn("id", ste.to_dict())
        self.assertIn("created_at", ste.to_dict())
        self.assertIn("updated_at", ste.to_dict())
        self.assertIn("__class__", ste.to_dict())

    def test_to_dict_has_added_attributes(self):
        ste = State()
        ste.middle_name = "Holberton"
        ste.my_number = 98
        self.assertEqual("Holberton", ste.middle_name)
        self.assertIn("my_number", ste.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        ste = State()
        ste_dict = ste.to_dict()
        self.assertEqual(str, type(ste_dict["id"]))
        self.assertEqual(str, type(ste_dict["created_at"]))
        self.assertEqual(str, type(ste_dict["updated_at"]))

    def test_to_dict_output(self):
        now = datetime.now()
        ste = State()
        ste.id = "123456"
        ste.created_at = ste.updated_at = now
        tdict = {
                'id': '123456',
                '__class__': 'State',
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
                }
        self.assertDictEqual(ste.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        ste = State()
        self.assertNotEqual(ste.to_dict(), ste.__dict__)

    def test_to_dict_using_arg(self):
        ste = State()
        with self.assertRaises(TypeError):
            ste.to_dict(None)


if __name__ == "__main__":
    unittest.main()
