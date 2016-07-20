#!/usr/bin/env python
# coding=utf-8

"""Attribute deletion test."""

from unittest import TestCase

from ..mapdata import (
    SimpleTestMapper, ArrayMapTestSchema, SimpleTestMapperWithClear,
    ArrayMapTestSchemaWithClear
)


class MapperDeletionValueFromFieldExceptionTest(TestCase):
    """Error Test due to field vlaue deletion."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapper
        self.data = self.cls.generate_test_data()
        del self.data.test.age
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_attr_delete_twice(self):
        """Re-deletion does nothing."""
        del self.mapper.age

    def test_field_deletion(self):
        """It raises nothing."""
        self.assertIn("age", self.mapper.fields)

    def test_data_value(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            print(self.data.test.age)

    def test_error_non_existence_attr(self):
        """The mapper should raise AttributeError."""
        with self.assertRaises(AttributeError):
            del self.mapper.test


class SimpleMapperDeletionTest(TestCase):
    """Field Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapper
        self.data = self.cls.generate_test_data()
        self.data_copy = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("age", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            self.data.test.age

    def test_other_values(self):
        """The other data shouldn't be removed."""
        self.assertEqual(self.data.test.name, self.data_copy.test.name)
        self.assertEqual(self.data.test.sex, self.data_copy.test.sex)

    def test_attr_reassign(self):
        """Re-assignment should work."""
        age = 24
        self.mapper.age = age
        self.assertEqual(self.data.test.age, age)


class SimpleMapperClearParentTest(TestCase):
    """Field based parent clear Test."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapperWithClear
        self.data = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)

    def test_clean(self):
        """self.data.test shouldn't exist."""
        del self.mapper.age
        self.assertTrue(
            hasattr(self.data, "test"),
            "The data should have test at this step."
        )
        del self.mapper.name
        self.assertTrue(
            hasattr(self.data, "test"),
            "The data should have test at this step."
        )
        del self.mapper.sex
        with self.assertRaises(AttributeError):
            print(self.data.test)


class SimpleMapperDictDeletionTest(TestCase):
    """Dict Based Field Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapper
        self.data = self.cls.generate_test_data(True)
        self.data_copy = self.cls.generate_test_data(True)
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("age", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(KeyError) as e:
            self.data["test"]["age"]
        self.assertEqual(str(e.exception), "'age'")

    def test_other_values(self):
        """The other data shouldn't be removed."""
        self.assertEqual(
            self.data["test"]["name"], self.data_copy["test"]["name"]
        )
        self.assertEqual(
            self.data["test"]["sex"], self.data_copy["test"]["sex"]
        )

    def test_attr_reassign(self):
        """Re-assignment should work."""
        age = 24
        self.mapper.age = age
        self.assertEqual(self.data["test"]["age"], age)


class DictMapperClearParentTest(TestCase):
    """Dict based field parent clear Test."""

    def setUp(self):
        """Setup."""
        self.cls = SimpleTestMapperWithClear
        self.data = self.cls.generate_test_data(True)
        self.mapper = self.cls(self.data)

    def test_clean(self):
        """self.data[test] shouldn't exist."""
        del self.mapper.age
        self.assertIn(
            "test", self.data,
            "The data should have test at this step."
        )
        del self.mapper.name
        self.assertIn(
            "test", self.data,
            "The data should have test at this step."
        )
        del self.mapper.sex
        self.assertNotIn("test", self.data)


class ArrayMapperDeletionTest(TestCase):
    """Array Element Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = ArrayMapTestSchema
        self.data = self.cls.generate_test_data()
        self.data_copy = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)
        del self.mapper.last_array

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("last_array", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(IndexError):
            self.data.test.array[1][2]

    def test_attr_reassign(self):
        """Re-assignment should work."""
        text = "This is a Test."
        self.mapper.last_array = text
        self.assertEqual(self.data.test.array[1][2], text)

    def test_other_values(self):
        """The other data shouldn't be removed."""
        self.assertEqual(
            self.data.test.array[0][0].correct,
            self.data_copy.test.array[0][0].correct
        )
        self.assertEqual(
            self.data.test.array[0][1].correct,
            self.data_copy.test.array[0][1].correct
        )
        self.assertEqual(
            self.data.test.array[1][0].correct,
            self.data_copy.test.array[1][0].correct
        )
        self.assertEqual(
            self.data.test.array[1][1].correct,
            self.data_copy.test.array[1][1].correct
        )


class ArraytMapperClearParentTest(TestCase):
    """Array element field parent clear Test."""

    def setUp(self):
        """Setup."""
        self.cls = ArrayMapTestSchemaWithClear
        self.data = self.cls.generate_test_data(False)
        self.mapper = self.cls(self.data)

    def test_last_element_remove(self):
        """self.data.test.array[2] shouldn't exist."""
        del self.mapper.last_first
        self.assertIsNotNone(
            self.data.test.array[2],
            "The data should have the array at this step."
        )
        del self.mapper.last_last
        self.assertIsNotNone(
            self.data.test.array[2],
            "The data should have the array at this step."
        )
        del self.mapper.last_mid
        with self.assertRaises(IndexError):
            print(self.data.test.array[2])

    def test_middle_element_remove(self):
        """self.data.test.array[1] should be None."""
        del self.mapper.mid_first
        self.assertIsNotNone(
            self.data.test.array[1],
            "The data should have the array at this step."
        )
        del self.mapper.mid_last
        self.assertIsNotNone(
            self.data.test.array[1],
            "The data should have the array at this step."
        )
        del self.mapper.mid_mid
        self.assertIsNone(self.data.test.array[1])

    def test_first_element_remove(self):
        """self.data.test.array[0] should be None."""
        del self.mapper.first_first
        self.assertIsNotNone(
            self.data.test.array[0],
            "The data should have the array at this step."
        )
        del self.mapper.first_last
        self.assertIsNotNone(
            self.data.test.array[0],
            "The data should have the array at this step."
        )
        del self.mapper.first_mid
        self.assertIsNone(self.data.test.array[0])

    def test_last_and_mid_element_remove(self):
        """len(self.data.test.array) should be 1."""
        del self.mapper.mid_first
        del self.mapper.mid_last
        del self.mapper.mid_mid
        del self.mapper.last_first
        del self.mapper.last_last
        del self.mapper.last_mid
        self.assertEqual(len(self.data.test.array), 1)
        self.assertListEqual(
            self.data.test.array[0],
            self.cls.generate_test_data().test.array[0]
        )

    def test_array_deletion(self):
        """self.data.test.array shouldn't exist."""
        del self.mapper.mid_first
        del self.mapper.mid_last
        del self.mapper.mid_mid
        del self.mapper.last_first
        del self.mapper.last_last
        del self.mapper.last_mid

        del self.mapper.first_first
        self.assertIsNotNone(
            self.data.test.array[0],
            "The data should have the array at this step."
        )
        del self.mapper.first_last
        self.assertIsNotNone(
            self.data.test.array[0],
            "The data should have the array at this step."
        )
        del self.mapper.first_mid
        with self.assertRaises(AttributeError):
            print(self.data.test.array)


class ArrayElementMapperDeletionTest(TestCase):
    """Array Field Deletion Test."""

    def setUp(self):
        """Setup."""
        self.cls = ArrayMapTestSchema
        self.data = self.cls.generate_test_data()
        self.data_copy = self.cls.generate_test_data()
        self.mapper = self.cls(self.data)
        del self.mapper.array

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertIn("array", self.mapper.fields)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            self.data.test.array[1][1].correct

    def test_attr_reassign(self):
        """Re-assignment should work."""
        text = "This is a Test."
        self.mapper.array = text
        self.assertEqual(self.data.test.array[1][1].correct, text)

    def test_other_values(self):
        """The other data shouldn't be removed."""
        self.assertEqual(
            self.data.test.array[1][2], self.data_copy.test.array[1][2]
        )
        self.assertEqual(
            self.data.test.array[0][0].correct,
            self.data_copy.test.array[0][0].correct
        )
        self.assertEqual(
            self.data.test.array[0][1].correct,
            self.data_copy.test.array[0][1].correct
        )
        self.assertEqual(
            self.data.test.array[1][0].correct,
            self.data_copy.test.array[1][0].correct
        )
