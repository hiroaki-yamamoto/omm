#!/usr/bin/env python
# coding=utf-8

"""Error checks for omm.Mapper."""

import unittest as ut

from ..mapdata import InconsistentTypeSchema


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
        from pprint import pprint
        pprint(result)
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
