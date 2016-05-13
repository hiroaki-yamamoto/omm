#!/usr/bin/env python
# coding=utf-8

"""MapField argument acceptance test."""

from unittest import TestCase

from omm import MapField


class ArgumentTest(TestCase):
    """Test case for argument."""

    def test_acceptance(self):
        """The field that is not acceptable should be treated as meta-data."""
        field = MapField(**{"$.this.is.not.acceptable": "Hello World"})
        self.assertEqual(
            getattr(field, "$.this.is.not.acceptable"), "Hello World"
        )
