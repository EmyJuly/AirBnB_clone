#!/usr/bin/python3
"""The unittests used for review.py

Unittest classes:
    TestReview_save
    TestReview_instantiation
    TestReview_to_dict
"""
import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.review import Review


class TestReview_save(unittest.TestCase):
    """The unittests testing the save method of class Review"""

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
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        self.assertLess(first_updated_at, rev.updated_at)

    def test_double_saves(self):
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        second_updated_at = rev.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rev.save()
        self.assertLess(second_updated_at, rev.updated_at)

    def test_save_with_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.save(None)

    def test_save_updates_file(self):
        rev = Review()
        rev.save()
        revid = "Review." + rev.id
        with open("file.json", "r") as f:
            self.assertIn(revid, f.read())


class TestReview_instantiation(unittest.TestCase):
    """The unittests testing instantiation of Review class"""

    def test_no_arguments_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_the_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_the_id_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_the_created_at_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_the_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rev))
        self.assertNotIn("place_id", rev.__dict__)

    def test_user_id_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rev))
        self.assertNotIn("user_id", rev.__dict__)

    def test_the_text_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rev))
        self.assertNotIn("text", rev.__dict__)

    def test_two_unique_reviews_ids(self):
        rev1 = Review()
        rev2 = Review()
        self.assertNotEqual(rev1.id, rev2.id)

    def test_two_different_reviews_created_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.created_at, rev2.created_at)

    def test_two_different_reviews_updated_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.updated_at, rev2.updated_at)

    def test_string_representation(self):
        now = datetime.now()
        now_repr = repr(now)
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = now
        revstr = rev.__str__()
        self.assertIn("[Review] (123456)", revstr)
        self.assertIn("'id': '123456'", revstr)
        self.assertIn("'created_at': " + now_repr, revstr)
        self.assertIn("'updated_at': " + now_repr, revstr)

    def test_unused_args(self):
        rev = Review(None)
        self.assertNotIn(None, rev.__dict__.values())

    def test_kwargs_instatiation(self):
        now = datetime.now()
        now_iso = now.isoformat()
        rev = Review(id="345", created_at=now_iso, updated_at=now_iso)
        self.assertEqual(rev.id, "345")
        self.assertEqual(rev.created_at, now)
        self.assertEqual(rev.updated_at, now)

    def test_instantiation_without_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_to_dict(unittest.TestCase):
    """The unittests testing the method to_dict in class Review"""

    def test_of_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_has_right_keys(self):
        rev = Review()
        self.assertIn("id", rev.to_dict())
        self.assertIn("created_at", rev.to_dict())
        self.assertIn("updated_at", rev.to_dict())
        self.assertIn("__class__", rev.to_dict())

    def test_to_dict_has_added_attributes(self):
        rev = Review()
        rev.middle_name = "Holberton"
        rev.my_number = 98
        self.assertEqual("Holberton", rev.middle_name)
        self.assertIn("my_number", rev.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        rev = Review()
        rev_dict = rev.to_dict()
        self.assertEqual(str, type(rev_dict["id"]))
        self.assertEqual(str, type(rev_dict["created_at"]))
        self.assertEqual(str, type(rev_dict["updated_at"]))

    def test_to_dict_output(self):
        now = datetime.now()
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = now
        tdict = {
                'id': '123456',
                '__class__': 'Review',
                'created_at': now.isoformat(),
                'updated_at': now.isoformat()
                }
        self.assertDictEqual(rev.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        rev = Review()
        self.assertNotEqual(rev.to_dict(), rev.__dict__)

    def test_to_dict_using_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.to_dict(None)


if __name__ == "__main__":
    unittest.main()
