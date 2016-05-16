#!/usr/bin/env python
# coding=utf-8

"""Error checks for omm.Mapper."""

import unittest as ut

from ..mapdata import InconsistentTypeSchema


class InconsistentTypesModelTest(ut.TestCase):
    """Test for inconsistent model."""

    def setUp(self):
        """Setup."""
        self.Schema = InconsistentTypeSchema

    def test_errors_property(self):
        """The errors should be shown."""
        schema = self.Schema(raise_inconsistent=False)
        self.assertDictEqual({
            "alias": [(
                "This field partially references the same path of name, "
                "but set_cast corresponding to \"(root)\" is not the same."
            ), (
                "This field partially references the same path of name, "
                "but set_cast corresponding to \"(root).test\" "
                "is not the same."
            ), (
                "This field partially references the same path of name, "
                "but set_cast corresponding to \"(root).test.user\" is"
                " not the same."
            ), (
                "This field partially references the same path of name, "
                "but set_cast corresponding to \"(root).root.test.user,name\""
                " is not the same."
            )],
            "display_name": [(
                "This field partially references the same path of name, "
                "but set_cast corresponding to \"(root).test\" "
                "is not the same."
            ), (
                "This field partially references the same path of name, "
                "but set_cast corresponding to \"(root).test.user\" is"
                " not the same."
            )]
        }, schema.errors)
