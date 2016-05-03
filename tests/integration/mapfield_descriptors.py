#!/usr/bin/env python
# coding=utf-8

"""
Map Field Descriptors tests.

Note that this spec is INTEGRATION TEST!
"""

import unittest as ut

from .mapdata import SimpleTestMapper, ArrayMapTestSchema
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


class DictArrayGetTest(ut.TestCase):
    """Accessed from Mapper object, but traget has array (target: dict)."""

    def setUp(self):
        """Setup the function."""
        self.data = ArrayMapTestSchema.generate_test_data(type_dict=True)
        self.schema = ArrayMapTestSchema(self.data)

    def test_array(self):
        """The returned value form the self.schema.array should be True."""
        self.assertIs(self.schema.array, True)
