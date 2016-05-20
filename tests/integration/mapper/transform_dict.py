#!/usr/bin/env python
# coding=utf-8

"""Serialization into/Deserialization from dict tests."""

import unittest as ut

from ..mapdata import (
    SimpleTestMapper, SimpleTestSchemaWithSimpleCast,
    SimpleTestSchemaWithSimpleCastWithDictFunction
)


class DictTransformInvocationTest(ut.TestCase):
    """Test for to_dict invocation."""

    def setUp(self):
        """Setup the function."""
        self.Schema = SimpleTestMapper
        self.connected_data = self.Schema.generate_test_data()
        self.expected_data = {
            "name": "Test Example",
            "age": 960,
            "sex": None
        }
        self.schema = self.Schema()

    def test_to_dict(self):
        """The return value of to_dict should be proper."""
        self.schema.connect(self.connected_data)
        result = self.schema.to_dict()
        self.assertDictEqual(self.expected_data, result)

    def test_to_dict_empty(self):
        """The return value of to_dict should be empty."""
        result = self.schema.to_dict()
        self.assertDictEqual({}, result)

    def test_from_dict(self):
        """The data should be deserialized properly."""
        # Honestly, from_dict doesn't needed because schema can recognize the
        # dict by putting as kwargs.
        result = self.Schema.from_dict(self.expected_data)
        self.assertIsInstance(result, self.Schema)
        self.assertEqual(result.name, self.expected_data["name"])
        self.assertEqual(result.age, self.expected_data["age"])
        self.assertEqual(result.sex, self.expected_data["sex"])


class DictTransformInvocationTestWithCasting(ut.TestCase):
    """Test for to_dict invocation with casting."""

    def setUp(self):
        """Setup the function."""
        self.Schema = SimpleTestSchemaWithSimpleCast
        self.connected_data = self.Schema.generate_test_data()
        self.expected_data = {"name": 41561234, "age": 199}
        self.schema = self.Schema()

    def test_to_dict(self):
        """The return value of to_dict should be proper."""
        self.schema.connect(self.connected_data)
        result = self.schema.to_dict()
        self.assertDictEqual(self.expected_data, result)

    def test_from_dict(self):
        """The data should be deserialized properly."""
        # Honestly, from_dict doesn't needed because schema can recognize the
        # dict by putting as kwargs.
        result = self.Schema.from_dict(self.expected_data)
        self.assertIsInstance(result, self.Schema)
        self.assertIsInstance(result.name, str)
        self.assertIsInstance(result.age, int)


class DictTransformInvocationTestWithCastingHavingDictFunc(ut.TestCase):
    """Test for to_dict invocation with casting."""

    def setUp(self):
        """Setup the function."""
        self.Schema = SimpleTestSchemaWithSimpleCastWithDictFunction
        self.connected_data = self.Schema.generate_test_data()
        self.expected_data = {"name": 41561234, "age": 199}
        self.schema = self.Schema()

    def test_to_dict(self):
        """The return value of to_dict should be proper."""
        self.schema.connect(self.connected_data)
        self.expected_data["name"] = str(self.expected_data["name"])
        result = self.schema.to_dict()
        self.assertDictEqual(self.expected_data, result)

    def test_from_dict(self):
        """The data should be deserialized properly."""
        # Honestly, from_dict doesn't needed because schema can recognize the
        # dict by putting as kwargs.
        result = self.Schema.from_dict(self.expected_data)
        self.assertIsInstance(result, self.Schema)
        self.assertIsInstance(result.name, self.Schema.StringField)
        self.assertIsInstance(result.age, self.Schema.IntegerField)
