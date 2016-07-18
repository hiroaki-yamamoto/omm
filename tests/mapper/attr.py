#!/usr/bin/env python
# coding=utf-8

"""Attribute deletion test."""

from unittest import TestCase, skip

import omm


@skip
class MapperDeletionTest(TestCase):
    """Field Deletion Test."""

    def setUp(self):
        """Setup."""
        class TestMap(omm.Mapper):
            name = omm.MapField("test.name")
            age = omm.MapField("test.age")
            sex = omm.MapField("test.sex")

        self.cls = TestMap
        self.mapper = self.cls(type("TestData", (object, ), {
            "test": type("TestSubData", (object, ), {
                "name": "Test Example",
                "age": 23,
                "sex": "test"
            })
        }))

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        del self.mapper.age
        self.assertNotIn("age", self.fields)

    def test_error_non_existence_attr(self):
        """The mapper should raise AttributeError."""
        with self.assertRaises(AttributeError):
            del self.mapper.test
