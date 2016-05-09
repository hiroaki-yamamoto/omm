#!/usr/bin/env python
# coding=utf-8

"""ModelField Casting test cases."""

from unittest import TestCase

from ..mapdata import (
    SimpleTestSchemaWithSimpleCast, ArrayMapCastingTestSchema
)


class ObjectBasedSimpleCastingTest(TestCase):
    """Simple casting test for object-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = SimpleTestSchemaWithSimpleCast
        self.data = self.Schema.generate_test_data()
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returned value should be the proper-type."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)


class ObjectBasedArrayCastingTest(TestCase):
    """Array casting test for object-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = ArrayMapCastingTestSchema
        self.data = self.Schema.generate_test_data()
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returne value should be the proper-value."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)
        self.assertIsInstance(self.schema.lastest_score, int)


class DictBasedSimpleCastingTest(TestCase):
    """Simple casting test for dict-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = SimpleTestSchemaWithSimpleCast
        self.data = self.Schema.generate_test_data(asdict=True)
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returned value should be the propert-type."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)


class DictBasedArrayCastingTest(TestCase):
    """Array casting test for object-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = ArrayMapCastingTestSchema
        self.data = self.Schema.generate_test_data(asdict=True)
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returne value should be the proper-value."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)
        self.assertIsInstance(self.schema.lastest_score, int)
