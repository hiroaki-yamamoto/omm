#!/usr/bin/env python
# coding=utf-8

"""Mapper errors property unit tests."""

import unittest as ut
import omm


class MapperNoErrorTest(ut.TestCase):
    """The map has no errors."""

    def setUp(self):
        """Setup the function."""
        class TestSchema(omm.Mapper):
            pass

        self.Schema = TestSchema
        self.schema = self.Schema()

    def test_error(self):
        """Should return proper error."""
        with self.assertRaises(NotImplementedError) as e:
            self.schema.errors
        self.assertEqual(str(e.exception), "Execute validate method.")
