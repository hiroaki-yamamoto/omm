#!/usr/bin/env python
# coding=utf-8

"""ModelField Casting test cases."""

from unittest import TestCase

from ..mapdata import (
    SimpleTestSchemaWithSimpleCast, ArrayMapCastingTestSchema,
    DictSimpleTestSchemaWithSimpleCast, ArrayMapDictCastingTestSchema,
    SimpleTestSchemaWithComplexCast1, SimpleTestSchemaWithComplexCast2,
    ArrayMapComplexCastingTestSchema, DictSimpleTestSchemaWithComplexCast1,
    DictSimpleTestSchemaWithComplexCast2, ArrayMapDictComplexCastingTestSchema,
    InvalidCastingLengthTestSchema
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
        self.assertIsInstance(self.schema.name, int)
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
        self.assertIsInstance(self.schema.name, int)
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
        self.assertIsInstance(self.schema.name, int)
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


class DictBasedComplexCastingTest(TestCase):
    """Complex casting test for dict-based connection."""

    def setUp(self):
        """Setup function."""
        self.Schema = DictSimpleTestSchemaWithComplexCast1
        self.schema = self.Schema()

    def test_set(self):
        """The objects should be typed properly."""
        self.schema.name = 189
        result = self.schema.connected_object
        self.assertIsInstance(result, self.Schema.TestObj1)
        self.assertIsInstance(result.test, dict)
        self.assertIsInstance(result.test["user"], self.Schema.TestObj2)
        self.assertIsInstance(result.test["user"].name, str)


class DictBasedComplexCastingTestWithFirstDict(TestCase):
    """Complex casting test for dict-based connection (2nd version)."""

    def setUp(self):
        """Setup function."""
        self.Schema = DictSimpleTestSchemaWithComplexCast2
        self.schema = self.Schema()

    def test_set(self):
        """The objects should be typed properly."""
        self.schema.name = 189
        result = self.schema.connected_object
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["test"], self.Schema.GeneratedObject)
        self.assertIsInstance(result["test"].user, dict)
        self.assertIsInstance(result["test"].user["name"], str)


class DictBasedArrayCastingTest(TestCase):
    """Array casting test for object-based schema."""

    def setUp(self):
        """Setup the function."""
        self.Schema = ArrayMapDictCastingTestSchema
        self.data = self.Schema.generate_test_data(asdict=True)
        self.schema = self.Schema(self.data)

    def test_get(self):
        """The returne value should be the proper-value."""
        self.assertIsInstance(self.schema.name, int)
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


class ArrayMapDictComplexArrayCastingTest(TestCase):
    """Test for complex casting with array (dict version)."""

    def setUp(self):
        """Setup function."""
        self.Schema = ArrayMapDictComplexCastingTestSchema
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


class InvalidCastLengthTest(TestCase):
    """Invalid casting length test."""

    def setUp(self):
        """Setup the function."""
        self.ObjectBasedSchema = InvalidCastingLengthTestSchema
        self.object_base = self.ObjectBasedSchema()

    def test_obj_name(self):
        """An error should be raised."""
        with self.assertRaises(ValueError) as error:
            self.object_base.name = "John Smith"
        self.assertEqual(
            str(error.exception),
            "The number of set_cast must be 4, not 3"
        )

    def test_obj_age(self):
        """An error should be raised."""
        with self.assertRaises(ValueError) as error:
            self.object_base.age = "18"
        self.assertEqual(
            str(error.exception),
            "The number of set_cast must be 4, not 5"
        )

    def test_admin_bit(self):
        """An error should be raised."""
        with self.assertRaises(ValueError) as error:
            self.object_base.admin_bit = "18"
        self.assertEqual(
            str(error.exception),
            "The number of set_cast must be 6, not 5"
        )

    def test_admin_manage_bit(self):
        """An error should be raised."""
        with self.assertRaises(ValueError) as error:
            self.object_base.manage_bit = False
        self.assertEqual(
            str(error.exception),
            "The number of set_cast must be 6, not 7"
        )
