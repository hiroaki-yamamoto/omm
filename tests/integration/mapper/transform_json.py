#!/usr/bin/env python
# coding=utf-8

"""JSON serializaton/desrialization tests."""

import json
import unittest as ut
from ..mapdata import SimpleTestMapper


class JSONSerializationTest(ut.TestCase):
    """Test case for json serialization/deserialization."""

    def setUp(self):
        """Setup function."""
        self.Schema = SimpleTestMapper
        self.test_data = self.Schema.generate_test_data()
        self.expected_data = {"name": "Test Example", "age": 960, "sex": None}
        self.schema = self.Schema()

    def test_serialization(self):
        """The return value of to_json should be proper."""
        self.schema.connect(self.test_data)
        result = json.loads(self.schema.to_json())
        self.assertDictEqual(self.expected_data, result)

    def test_empty_schema(self):
        """The return value of to_json should be empty."""
        result = json.loads(self.schema.to_json())
        self.assertDictEqual({}, result)

    def test_deserialization(self):
        """The return value of from_json should be proper."""
        result = self.Schema.from_json(json.dumps(self.expected_data))
        self.assertIsInstance(result, self.Schema)
        self.assertEqual(result.name, self.expected_data["name"])
        self.assertEqual(result.age, self.expected_data["age"])
        self.assertEqual(result.sex, self.expected_data["sex"])
