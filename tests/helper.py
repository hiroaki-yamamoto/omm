#!/usr/bin/env python
# coding=utf-8

"""Helper tests."""

import omm.helper
import unittest as ut
try:
    from unittest.mock import MagicMock, call
except ImportError:
    from mock import MagicMock, call


class ReduceWithoutInitTest(ut.TestCase):
    """Test for reduce(fn, it) test."""

    def setUp(self):
        """Setup function."""
        self.func = MagicMock(
            side_effect=lambda x, y, index: y
        )
        self.data = [1, 2, 3, 4]

    def test_call_reduce(self):
        """The function should be called properly."""
        omm.helper.reduce_with_index(self.func, self.data)
        self.assertEqual(self.func.call_count, 3)
        self.func.assert_has_calls([
            call(1, 2, 0), call(2, 3, 1), call(3, 4, 2)
        ])


class ReduceErrorTest(ut.TestCase):
    """Test for reduce(fn, it) test, but it is empty."""

    def setUp(self):
        """Setup function."""
        self.func = MagicMock(
            side_effect=lambda x, y, index: y
        )
        self.data = []

    def test_call_reduce(self):
        """The function should be called properly."""
        with self.assertRaises(TypeError) as e:
            omm.helper.reduce_with_index(self.func, self.data)
        self.assertEqual(
            str(e.exception),
            "reduce_with_index() of empty sequence with no initial value"
        )
        self.assertFalse(self.func.called)
