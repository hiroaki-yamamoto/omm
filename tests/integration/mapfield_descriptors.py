#!/usr/bin/env python
# coding=utf-8

"""
Map Field Descriptors tests.

Note that this spec is INTEGRATION TEST!
"""

import unittest as ut

from .mapdata import SimpleTestMapper
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

    def test_cls_test(self):
        """MapField should return itself when it is accessed from class."""
        self.assertIsInstance(SimpleTestMapper.name, MapField)
        self.assertIsInstance(SimpleTestMapper.age, MapField)
        self.assertIsInstance(SimpleTestMapper.sex, MapField)


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

    def test_cls_test(self):
        """MapField should return itself when it is accessed from class."""
        self.assertIsInstance(SimpleTestMapper.name, MapField)
        self.assertIsInstance(SimpleTestMapper.age, MapField)
        self.assertIsInstance(SimpleTestMapper.sex, MapField)
