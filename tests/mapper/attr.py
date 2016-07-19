#!/usr/bin/env python
# coding=utf-8

"""Attribute deletion test."""

from unittest import TestCase

from ..mapdata import SimpleTestMapper, ArrayMapTestSchema


class MapperDeletionValueFromFieldExceptionTest(TestCase):
    """Error Test due to field vlaue deletion."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapper
        self.data = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_attr_delete_twice(self):
        """Re-deletion doesn nothing."""
        del self.mapper.age

    def test_field_deletion(self):
        """It raises nothing."""
        self.assertIn("age", self.mapper.fields)

    def test_data_value(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            self.data.test.age

    def test_error_non_existence_attr(self):
        """The mapper should raise AttributeError."""
        with self.assertRaises(AttributeError):
            del self.mapper.test


class SimpleMapperDeletionTest(TestCase):
    """Field Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapper
        self.data = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("age", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            self.data.test.age

    def test_attr_reassign(self):
        """Re-assignment should work."""
        age = 24
        self.mapper.age = age
        self.assertEqual(self.data.test.age, age)


class SimpleMapperDictDeletionTest(TestCase):
    """Dict Based Field Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapper
        self.data = self.cls.generate_test_data(True)
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("age", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(KeyError) as e:
            self.data["test"]["age"]
        self.assertEqual(str(e.exception), "'age'")

    def test_attr_reassign(self):
        """Re-assignment should work."""
        age = 24
        self.mapper.age = age
        self.assertEqual(self.data["test"]["age"], age)


class ArrayMapperDeletionTest(TestCase):
    """Array Element Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = ArrayMapTestSchema
        self.data = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)
        del self.mapper.last_array

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("last_array", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(IndexError):
            self.data.test.array[1][2]

    def test_attr_reassign(self):
        """Re-assignment should work."""
        text = "This is a Test."
        self.mapper.last_array = text
        self.assertEqual(self.data.test.array[1][2], text)


class ArrayElementMapperDeletionTest(TestCase):
    """Array Field Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = ArrayMapTestSchema
        self.data = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)
        del self.mapper.array

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("array", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            self.data.test.array[1][1].correct

    def test_attr_reassign(self):
        """Re-assignment should work."""
        text = "This is a Test."
        self.mapper.array = text
        self.assertEqual(self.data.test.array[1][1].correct, text)
