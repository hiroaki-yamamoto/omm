#!/usr/bin/env python
# coding=utf-8

"""Metadata check."""

import unittest as ut

import omm


class MapperMetadataTest(ut.TestCase):
    """Metadata check."""

    def setUp(self):
        """Setup function."""
        class TestSchema(omm.Mapper):
            name = omm.MapField("test.name")

        self.Schema = TestSchema
        self.kwargs = {
            "name": "This is a test",
            "metadata": {
                "test": True
            }
        }
        self.schema = TestSchema(**self.kwargs)

    def test_meta(self):
        """The data should be stored to the schema."""
        self.assertEqual(self.schema.name, self.kwargs["name"])
        self.assertDictEqual(self.kwargs["metadata"], self.schema.metadata)
