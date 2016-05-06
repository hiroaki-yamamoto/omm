#!/usr/bin/env python
# coding=utf-8

"""
Map Field Descriptors tests.

Note that this spec is INTEGRATION TEST!
"""

import unittest as ut

from .mapdata import (
    SimpleTestMapper, DictSimpleTestSchema,
    ArrayMapTestSchema, ArrayMapDictTestSchema
)
from omm import MapField


class ObjectGetTest(ut.TestCase):
    """MapField.__get__ test (object)."""

    def setUp(self):
        """Setup the function."""
        self.data = SimpleTestMapper.generate_test_data()
        self.schema = SimpleTestMapper(self.data)

    def test_schema_data(self):
        """self.schema should return the value of the data."""
        self.assertEqual(self.schema.name, self.data.test.name)
        self.assertEqual(self.schema.age, self.data.test.age)
        self.assertEqual(self.schema.sex, self.data.test.sex)


class ObjectSetTest(ut.TestCase):
    """MapField.__set__ test (object)."""

    def setUp(self):
        """Setup the function."""
        self.schema = SimpleTestMapper()

    def test_set(self):
        """set descriptor should work properly."""
        self.schema.name = "Test"
        self.schema.age = 28
        self.schema.sex = None

        obj = self.schema.connected_object
        self.assertEqual(obj.test.name, self.schema.name)
        self.assertEqual(obj.test.age, self.schema.age)
        self.assertEqual(obj.test.sex, self.schema.sex)


class DictGetTest(ut.TestCase):
    """MapField.__get__ test (dict)."""

    def setUp(self):
        """Setup the function."""
        self.data = SimpleTestMapper.generate_test_data(type_dict=True)
        self.schema = SimpleTestMapper(self.data)

    def test_schema_data(self):
        """self.schema should return the value of the data."""
        self.assertEqual(self.schema.name, self.data["test"]["name"])
        self.assertEqual(self.schema.age, self.data["test"]["age"])
        self.assertEqual(self.schema.sex, self.data["test"]["sex"])


class DictSetTest(ut.TestCase):
    """MapField.__set__ test (dict)."""

    def setUp(self):
        """Setup function."""
        self.schema = DictSimpleTestSchema()

    def test_set(self):
        """Setup set."""
        self.schema.name = "Test"
        self.schema.age = 28
        self.schema.sex = None

        self.assertDictEqual({
            "test": {
                "name": self.schema.name,
                "age": self.schema.age,
                "sex": self.schema.sex
            }
        }, self.schema.connected_object)


class ClsGetTest(ut.TestCase):
    """MapField.__get__ test (accessed from Mapper class declaration)."""

    def setUp(self):
        """Setup the function."""
        self.schema = SimpleTestMapper

    def test_cls_test(self):
        """MapField should return itself when it is accessed from class."""
        self.assertIsInstance(self.schema.name, MapField)
        self.assertIsInstance(self.schema.age, MapField)
        self.assertIsInstance(self.schema.sex, MapField)


class ObjArrayGetTest(ut.TestCase):
    """Accessed from Mapper object, but target has array (target: obj)."""

    def setUp(self):
        """Setup the function."""
        self.data = ArrayMapTestSchema.generate_test_data()
        self.schema = ArrayMapTestSchema(self.data)

    def test_array(self):
        """The returned value form the self.schema.array should be True."""
        self.assertIs(self.schema.array, True)


class ObjectArraySetTest(ut.TestCase):
    """Unit test for setting value to the mapping field."""

    def setUp(self):
        """Setup the test."""
        self.schema = ArrayMapTestSchema()

    def test_array(self):
        """The connected value should be proper."""
        self.schema.array = True
        result = self.schema.connected_object
        self.assertIsNone(result.test.array[0])
        self.assertIsNone(result.test.array[1][0])
        self.assertIs(result.test.array[1][1].correct, True)


class DictArrayGetTest(ut.TestCase):
    """Accessed from Mapper object, but traget has array (target: dict)."""

    def setUp(self):
        """Setup the function."""
        self.data = ArrayMapTestSchema.generate_test_data(type_dict=True)
        self.schema = ArrayMapTestSchema(self.data)

    def test_array(self):
        """The returned value form the self.schema.array should be True."""
        self.assertIs(self.schema.array, True)


class DictArraySetTest(ut.TestCase):
    """Unit test for setting value to the mapping field."""

    def setUp(self):
        """Setup the test."""
        self.schema = ArrayMapDictTestSchema()

    def test_array(self):
        """The connected value should be proepr."""
        self.schema.array = True
        result = self.schema.connected_object
        self.assertIsNone(result["test"]["array"][0])
        self.assertIsNone(result["test"]["array"][1][0])
        self.assertIs(result["test"]["array"][1][1]["correct"], True)
