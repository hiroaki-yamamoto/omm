#!/usr/bin/env python
# coding=utf-8

"""Normal map unit tests."""

from unittest import TestCase

import omm


class MappingFieldInitTest(TestCase):
    """MappingField is properly initialized."""

    def setUp(self):
        """Set up the class."""
        self.target = "mapping.test"
        self.field = omm.MapField(self.target)

    def test_assignment(self):
        """The field should have mapping target."""
        self.assertEqual(self.target, self.field.target)


class MappingFieldLazyInitTest(TestCase):
    """Mapping Field should assign the mapping after initialization."""

    def setUp(self):
        """Set up the class."""
        self.target = "mapping.test"
        self.field = omm.MapField()
        self.field.target = self.target

    def test_assignment(self):
        """The field should have mapping target."""
        self.assertEqual(self.target, self.field.target)
