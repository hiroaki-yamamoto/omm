#!/usr/bin/env python
# coding=utf-8

"""Error checks for omm.Mapper."""

import unittest as ut

try:
    from unittest.mock import MagicMock
except:
    from mock import MagicMock

import omm

from ..mapdata import InconsistentTypeSchema, ArrayInconsistentTypeSchema


class InconsistentTypesModelTest(ut.TestCase):
    """Test for inconsistent model."""

    def setUp(self):
        """Setup."""
        self.maxDiff = None
        self.Schema = InconsistentTypeSchema

    def test_errors_property(self):
        """The errors should be shown."""
        schema = self.Schema()
        setattr(schema, "$testing$", True)
        self.assertFalse(schema.validate())
        result = schema.errors
        error_msg = (
            "This field partially references the same path of "
            "{}, but set_cast corresponding to \"{}\" "
            "is not the same."
        )
        self.assertDictEqual({
            "display_name": [
                error_msg.format("alias", "(root)"),
                error_msg.format("alias", "(root).test.user.name")
            ],
            "name": [
                error_msg.format("alias", "(root)"),
                error_msg.format("alias", "(root).test"),
                error_msg.format("alias", "(root).test.user"),
                error_msg.format("alias", "(root).test.user.name")
            ]
        }, result)


class InconsistentTypesArrayModelTest(ut.TestCase):
    """Test for inconsistent model."""

    def setUp(self):
        """Setup."""
        self.maxDiff = None
        self.Schema = ArrayInconsistentTypeSchema

    def test_errors_property(self):
        """The errors should be shown."""
        schema = self.Schema()
        setattr(schema, "$testing$", True)
        self.assertFalse(schema.validate())
        result = schema.errors
        error_msg = (
            "This field partially references the same path of "
            "{}, but set_cast corresponding to \"{}\" "
            "is not the same."
        )
        self.assertDictEqual({
            "name": [
                error_msg.format("alias", "(root).test.users"),
                error_msg.format("alias", "(root).test.users.0"),
                error_msg.format("alias", "(root).test.users.0.1.name")
            ]
        }, result)


class FieldValidationTest(ut.TestCase):
    """validate() for each field should be called."""

    def setUp(self):
        """Setup the function."""
        class TestSchema(omm.Mapper):
            test = omm.MapField("test.example")
            test2 = omm.MapField("test.example2")

            def __new__(cls, *args, **kwargs):
                cls.test.validate = MagicMock(
                    side_effect=ValueError("It works")
                )
                cls.test2.validate = MagicMock(
                    side_effect=ValueError("It works")
                )
                return super(TestSchema, cls).__new__(cls, *args, **kwargs)

        self.Schema = TestSchema
        self.schema = self.Schema()

    def test_validate(self):
        """The validation should be failed."""
        self.assertFalse(self.schema.validate())
        result = self.schema.errors
        self.assertDictEqual(
            {"test": ["It works"], "test2": ["It works"]},
            result
        )
