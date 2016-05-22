#!/usr/bin/env python
# coding=utf-8

"""JSON serialization/deserialization unit tests."""

import json
import unittest as ut
try:
    from unittest.mock import MagicMock, call
except ImportError:
    from mock import MagicMock, call

import omm


class JSONInValueInvocationTest(ut.TestCase):
    """Test for calling (to|from)_json in the casted value."""

    def setUp(self):
        """Setup function."""
        class TestField(object):
            def __new__(cls, value):
                cls.to_json = MagicMock(return_value=json.dumps(
                    {"value": value})
                )
                cls.to_dict = MagicMock(return_value={"value": value})
                return super(TestField, cls).__new__(cls)

            def __init__(self, value):
                self.value = value
                super(TestField, self).__init__()

            from_json = MagicMock(
                side_effect=lambda jstr: TestField(
                    list(json.loads(jstr).values())[0]["value"]
                )
            )
            from_dict = MagicMock(
                side_effect=lambda dct: TestField(dct.values()[0]["value"])
            )

        class TestSchema(omm.Mapper):
            GeneratedObject = type("GeneratedObject", (object, ), {})
            name = omm.MapField(
                "test.user.map", get_cast=TestField, set_cast=TestField
            )
            age = omm.MapField(
                "test2.user.age",
                get_cast=TestField,
                set_cast=[
                    GeneratedObject, GeneratedObject,
                    GeneratedObject, TestField
                ]
            )

        self.Schema = TestSchema
        self.Field = TestField
        self.schema = self.Schema(name="test", age=15)
        self.data = {"name": {"value": "test"}, "age": {"value": 15}}

    def test_to_json(self):
        """Field.to_json should be called."""
        self.schema.to_json()
        self.assertEqual(self.Field.to_json.call_count, 2)
        self.Field.to_json.assert_has_calls([call(), call()])
        self.Field.to_dict.assert_not_called()

    def test_from_json(self):
        """Field.from_json should be called."""
        jsonstr = json.dumps(self.data)
        self.Schema.from_json(jsonstr)
        self.assertEqual(self.Field.from_json.call_count, 2)
        self.Field.from_json.assert_has_calls(
            [
                call(json.dumps({"name": self.data["name"]})),
                call(json.dumps({"age": self.data["age"]}))
            ], any_order=True
        )
        self.Field.from_dict.assert_not_called()


class DictInvocationAsAlternativeTest(ut.TestCase):
    """Test for to_dict invocation."""

    def setUp(self):
        """Setup function."""
        class TestField(object):
            def __new__(cls, value):
                cls.to_dict = MagicMock(return_value={"value": value})
                return super(TestField, cls).__new__(cls)

            def __init__(self, value):
                self.value = value
                super(TestField, self).__init__()

            from_dict = MagicMock(
                side_effect=lambda dct: TestField(
                    list(dct.values())[0]["value"]
                )
            )

        class TestSchema(omm.Mapper):
            GeneratedObject = type("GeneratedObject", (object, ), {})
            name = omm.MapField(
                "test.user.map", get_cast=TestField, set_cast=TestField
            )
            age = omm.MapField(
                "test2.user.age",
                get_cast=TestField,
                set_cast=[
                    GeneratedObject, GeneratedObject,
                    GeneratedObject, TestField
                ]
            )
        self.Schema = TestSchema
        self.Field = TestField
        self.schema = self.Schema(name="test", age=15)
        self.data = {"name": {"value": "test"}, "age": {"value": 15}}

    def test_to_dict(self):
        """Field.to_dict should be called if to_json doesn't exist."""
        self.schema.to_json()
        self.assertEqual(self.Field.to_dict.call_count, 2)
        self.Field.to_dict.assert_has_calls([call(), call()])

    def test_from_dict(self):
        """Field.from_dict should be called if to_dict doesn't exist."""
        jsonstr = json.dumps(self.data)
        self.Schema.from_json(jsonstr)
        self.assertEqual(self.Field.from_dict.call_count, 2)
        self.Field.from_dict.assert_has_calls(
            [
                call({"name": self.data["name"]}),
                call({"age": self.data["age"]})
            ], any_order=True
        )
