#!/usr/bin/env python
# coding=utf-8

"""ModelField Casting test cases."""

from unittest import TestCase

from ..mapdata import (
    SimpleTestSchemaWithSimpleCast, ArrayMapCastingTestSchema,
    DictSimpleTestSchemaWithSimpleCast, ArrayMapDictCastingTestSchema,
    SimpleTestSchemaWithComplexCast1, SimpleTestSchemaWithComplexCast2,
    ArrayMapComplexCastingTestSchema
)


class ObjectBasedSimpleCastingTest(TestCase):
    """Simple casting test for object-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = SimpleTestSchemaWithSimpleCast
        self.data = self.Schema.generate_test_data()
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returned value should be the proper-type."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)

    def test_set(self):
        """
        The name should be str.

        self.schema.connected_object.name should be
        casted into the specified type.
        """
        self.schema.name = 0xabcdef
        self.assertIsInstance(
            self.schema.connected_object.test.user.name, str
        )


class ObjectBasedComplexCastingTest(TestCase):
    """Complex casting test for object-based connection."""

    def setUp(self):
        """Setup function."""
        self.Schema = SimpleTestSchemaWithComplexCast1
        self.schema = self.Schema()

    def test_set(self):
        """The objects should be typed properly."""
        self.schema.name = 189
        result = self.schema.connected_object
        self.assertIsInstance(result, self.Schema.TestObj1)
        self.assertIsInstance(result.test, dict)
        self.assertIsInstance(result.test["user"], self.Schema.TestObj2)
        self.assertIsInstance(result.test["user"].name, str)


class ObjectBasedComplexCastingTestWithFirstDict(TestCase):
    """Complex casting test for object-based connection (2nd version)."""

    def setUp(self):
        """Setup function."""
        self.Schema = SimpleTestSchemaWithComplexCast2
        self.schema = self.Schema()

    def test_set(self):
        """The objects should be typed properly."""
        self.schema.name = 189
        result = self.schema.connected_object
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["test"], self.Schema.GeneratedObject)
        self.assertIsInstance(result["test"].user, dict)
        self.assertIsInstance(result["test"].user["name"], str)


class ObjectBasedArrayCastingTest(TestCase):
    """Array casting test for object-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = ArrayMapCastingTestSchema
        self.data = self.Schema.generate_test_data()
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returne value should be the proper-value."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)
        self.assertIsInstance(self.schema.lastest_score, int)

    def test_set(self):
        """
        The name should be str.

        self.schema.connected_object.name should be
        casted into the specified type.
        """
        self.schema.name = 0xabcdef
        self.assertIsInstance(
            self.schema.connected_object.users[1][1].name, str
        )


class ObjectBasedArrayComplexCastingTest(TestCase):
    """Test for complex casting with array."""

    def setUp(self):
        """Setup function."""
        self.Schema = ArrayMapComplexCastingTestSchema
        self.schema = self.Schema()

    def test_setter(self):
        """
        The stored value should be properly.

        Calling setter descriptor, the value should be stored with
        proper values, including its parents.
        """
        self.schema.name = "test"
        result = self.schema.connected_object
        self.assertIsInstance(result, self.Schema.StartObj)
        self.assertIsInstance(result.test, self.Schema.TestObj)
        self.assertIsInstance(result.test.users, self.Schema.Users)
        self.assertIsInstance(result.test.users[0], self.Schema.UserProfiles)
        self.assertIsInstance(result.test.users[0][1], self.Schema.Profile)
        self.assertIsInstance(
            result.test.users[0][1].info, self.Schema.InfoObj
        )
        self.assertIsInstance(result.test.users[0][1].info["name"], str)


class DictBasedSimpleCastingTest(TestCase):
    """Simple casting test for dict-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = DictSimpleTestSchemaWithSimpleCast
        self.data = self.Schema.generate_test_data(asdict=True)
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returned value should be the propert-type."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)

    def test_set(self):
        """
        The name should be str.

        self.schema.connected_object.name should be
        casted into the specified type.
        """
        self.schema.name = 0xabcdef
        self.assertIsInstance(
            self.schema.connected_object["test"]["user"]["name"], str
        )


class DictBasedArrayCastingTest(TestCase):
    """Array casting test for object-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = ArrayMapDictCastingTestSchema
        self.data = self.Schema.generate_test_data(asdict=True)
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returne value should be the proper-value."""
        self.assertIsInstance(self.schema.name, str)
        self.assertIsInstance(self.schema.age, int)
        self.assertIsInstance(self.schema.lastest_score, int)

    def test_set(self):
        """
        The name should be str.

        self.schema.connected_object.name should be
        casted into the specified type.
        """
        self.schema.name = 0xabcdef
        self.assertIsInstance(
            self.schema.connected_object["users"][1][1]["name"], str
        )
