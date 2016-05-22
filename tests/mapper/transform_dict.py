#!/usr/bin/env python
# coding=utf-8

"""Dict transformation unit tests."""

import unittest as ut
try:
    from unittest.mock import MagicMock, call
except ImportError:
    from mock import MagicMock, call

import omm


class DictCastingInvocationTest(ut.TestCase):
    """Unit test for to_dict at the cast invocation test."""

    def setUp(self):
        """Setuo function."""
        class TestField(object):
            def __new__(cls, value):
                cls.to_dict = MagicMock(return_value=value)
                return super(TestField, cls).__new__(cls)

            def __init__(self, value):
                self.value = value

            from_dict = MagicMock(
                side_effect=lambda dct: TestField(list(dct.values())[0])
            )

        class TestMapper(omm.Mapper):
            GenObj = type("GenObj", (object,), {})
            test = omm.MapField(
                "test", get_cast=TestField, set_cast=TestField
            )
            test2 = omm.MapField(
                "test2.user.test", get_cast=TestField,
                set_cast=[GenObj, GenObj, GenObj, TestField]
            )

        self.Schema = TestMapper
        self.Field = TestField
        self.schema = self.Schema()

    def test_to_dict(self):
        """self.Field.to_dict should be called."""
        self.schema.test = "test"
        self.schema.to_dict()
        self.Field.to_dict.assert_called_once_with()

    def test_from_dict(self):
        """self.Field.from_dict should be called with peoper-value."""
        self.Schema.from_dict({
            "test": "This is a test",
            "test2": "2nd",
            "test3": "talaaaan!"
        })
        self.assertEqual(self.Field.from_dict.call_count, 2)
        self.Field.from_dict.assert_has_calls(
            [call({"test": "This is a test"}), call({"test2": "2nd"})],
            any_order=True
        )
