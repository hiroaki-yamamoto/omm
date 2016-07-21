#!/usr/bin/env python
# coding=utf-8

"""Dump and Load functionality tests."""

from unittest import TestCase
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from ..mapdata import SimpleTestMapper


class DumpsTest(TestCase):
    """Dumps test."""

    def setUp(self):
        """Setup."""
        self.serialization = MagicMock()
        self.mapper = SimpleTestMapper()
        self.mapper.to_dict = MagicMock()

    def test_dumps(self):
        """Serialize function should return proper value."""
        result = self.mapper.dumps(self.serialization)
        self.mapper.to_dict.assert_called_once_with()
        self.serialization.assert_called_once_with(
            self.mapper.to_dict.return_value
        )
        self.assertIs(result, self.serialization.return_value)


class LoadsTest(TestCase):
    """Loads test."""

    def setUp(self):
        """Setup."""
        self.deser_fn = MagicMock()
        self.mapper = SimpleTestMapper
        self.mapper.from_dict = MagicMock()

    def test_dumps(self):
        """Serialize function should return proper value."""
        data = "something"
        result = self.mapper.loads(self.deser_fn, data)
        self.mapper.from_dict.assert_called_once_with(
            self.deser_fn.return_value
        )
        self.deser_fn.assert_called_once_with(data)
        self.assertIs(result, self.mapper.from_dict.return_value)
