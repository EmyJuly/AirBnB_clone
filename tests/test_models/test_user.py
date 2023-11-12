#!/usr/bin/python3
"""The unittests testing for models/user.py

Unittest classes:
TestUser_save
TestUser_instantiation
TestUser_to_dict
"""

import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.user import User


class TestUser_save(unittest.TestCase):
    """The unittests testing the save method of class User"""

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
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        self.assertLess(first_updated_at, usr.updated_at)

    def test_double_saves(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        second_updated_at = usr.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        usr.save()
        self.assertLess(second_updated_at, usr.updated_at)

    def test_save_with_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.save(None)

    def test_save_updates_file(self):
        usr = User()
        usr.save()
        usrid = "User." + usr.id
        with open("file.json", "r") as f:
            self.assertIn(usrid, f.read())


class TestUser_instantiation(unittest.TestCase):
    """The unittests testing instantiation of User class"""

    def test_no_arguments_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_the_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_the_id_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_the_created_at_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_the_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_the_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_the_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_the_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_the_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_unique_users_ids(self):
        usr1 = User()
        usr2 = User()
        self.assertNotEqual(usr1.id, usr2.id)

    def test_two_different_users_created_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.created_at, usr2.created_at)

    def test_two_different_users_updated_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.updated_at, usr2.updated_at)

    def test_string_representation(self):
        now = datetime.now()
        now_repr = repr(now)
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = now
        usrstr = usr.__str__()
        self.assertIn("[User] (123456)", usrstr)
        self.assertIn("'id': '123456'", usrstr)
        self.assertIn("'created_at': " + now_repr, usrstr)
        self.assertIn("'updated_at': " + now_repr, usrstr)

    def test_unused_args(self):
        usr = User(None)
        self.assertNotIn(None, usr.__dict__.values())

    def test_kwargs_instatiation(self):
        now = datetime.now()
        now_iso = now.isoformat()
        usr = User(id="345", created_at=now_iso, updated_at=now_iso)
        self.assertEqual(usr.id, "345")
        self.assertEqual(usr.created_at, now)
        self.assertEqual(usr.updated_at, now)

    def test_instantiation_without_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_to_dict(unittest.TestCase):
    """The unittests testing the method to_dict in class User"""

    def test_of_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_has_right_keys(self):
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())

    def test_to_dict_has_added_attributes(self):
        usr = User()
        usr.middle_name = "Holberton"
        usr.my_number = 98
        self.assertEqual("Holberton", usr.middle_name)
        self.assertIn("my_number", usr.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        usr = User()
        usr_dict = usr.to_dict()
        self.assertEqual(str, type(usr_dict["id"]))
        self.assertEqual(str, type(usr_dict["created_at"]))
        self.assertEqual(str, type(usr_dict["updated_at"]))

    def test_to_dict_output(self):
        now = datetime.now()
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = now
        tdict = {
                'id': '123456',
                '__class__': 'User',
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
                }
        self.assertDictEqual(usr.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        usr = User()
        self.assertNotEqual(usr.to_dict(), usr.__dict__)

    def test_to_dict_using_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()
