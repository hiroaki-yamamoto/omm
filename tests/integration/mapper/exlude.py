#!/usr/bin/env python
# coding=utf-8

"""Serialization / deserializatoin exclusion check."""

import json
from unittest import TestCase

import omm
from ...mapdata import SimpleTestMapper


class SimpleExclusionTest(TestCase):
    """Simple Exclusion case."""

    def setUp(self):
        """Setup."""
        class ExclusionMapper(SimpleTestMapper):
            age = omm.MapField("test.age", exclude=True)

        self.cls = ExclusionMapper
        self.data = self.cls(self.cls.generate_test_data(True))
        self.dct = {
            "name": self.data.name,
            "age": self.data.age,
            "sex": self.data.sex
        }

    def test_to_json(self):
        """Should serialize the data into JSON except age field."""
        result = json.loads(self.data.to_json())
        self.assertNotIn("age", result)

    def test_from_json(self):
        """Should deserialize the data into JSON except age field."""
        result = self.cls.from_json(json.dumps(self.dct))
        with self.assertRaises(AttributeError):
            print(result.age)


class SpecificExclusionTypeTest(TestCase):
    """Exclusion case with exclusion type dict."""

    def setUp(self):
        """Setup."""
        class ExclusionMapper(SimpleTestMapper):
            age = omm.MapField(
                "test.age", exclude={"json": True, "dict": False}
            )

        self.cls = ExclusionMapper
        self.data = self.cls(self.cls.generate_test_data(True))
        self.dct = {
            "name": self.data.name,
            "age": self.data.age,
            "sex": self.data.sex
        }

    def test_to_json(self):
        """Should serialize the data into JSON except age field."""
        result = json.loads(self.data.to_json())
        self.assertNotIn("age", result)

    def test_from_json(self):
        """Should deserialize the data into JSON except age field."""
        result = self.cls.from_json(json.dumps(self.dct))
        with self.assertRaises(AttributeError):
            print(result.age)

    def test_to_dict(self):
        """Should serialize the data into JSON except age field."""
        result = self.data.to_dict()
        self.assertIn("age", result)

    def test_from_dict(self):
        """Should deserialize the data into JSON except age field."""
        result = self.cls.from_dict(self.dct)
        self.assertEqual(result.age, self.dct["age"])


class MethodBasedExclusionTest(TestCase):
    """Simple Exclusion case."""

    def setUp(self):
        """Setup."""
        class ExclusionMapper(SimpleTestMapper):
            age = omm.MapField("test.age", exclude_serialize=True)
            name = omm.MapField("test.name", exclude_deserialize=True)

        self.cls = ExclusionMapper
        self.data = self.cls(self.cls.generate_test_data(True))
        self.dct = {
            "name": self.data.name,
            "age": self.data.age,
            "sex": self.data.sex
        }

    def test_serialization(self):
        """The result shouldn't contain age, but should contain name."""
        result = json.loads(self.data.to_json())
        self.assertNotIn("age", result)
        self.assertIn("name", result)

    def test_deserialization(self):
        """The result shouldn't contain name, but should contain age."""
        result = self.cls.from_json(json.dumps(self.dct))
        with self.assertRaises(AttributeError):
            print(result.name)
        self.assertEqual(result.age, self.dct["age"])
