#!/usr/bin/env python
# coding=utf-8

"""Attribute deletion test."""

from unittest import TestCase

import omm


class MapperDeletionTest(TestCase):
    """Field Deletion Test."""

    def setUp(self):
        """Setup."""
        class TestMap(omm.Mapper):
            name = omm.MapField("test.name")
            age = omm.MapField("test.age")
            sex = omm.MapField("test.sex")

        class DataCls(object):

            class DataSubCls(object):

                def __init__(self):
                    self.name = "Test Example"
                    self.age = 23
                    self.sex = "test"

            def __init__(self):
                self.test = self.DataSubCls()

        self.cls = TestMap
        self.data_cls = DataCls
        self.data = DataCls()
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_field_deletion(self):
        """The field lists of mapper shouldn't have the corresponding field."""
        self.assertNotIn("age", self.mapper.fields)
        self.assertNotIn("age", self.mapper.__dict__)
        self.assertEqual(self.data.test.age, self.data_cls.DataSubCls().age)

    def test_error_non_existence_attr(self):
        """The mapper should raise AttributeError."""
        with self.assertRaises(AttributeError):
            del self.mapper.test


class MapperDeletionValueFromFieldTest(TestCase):
    """Field Deletion by specified metadata from field with value Test."""

    def setUp(self):
        """Setup."""
        class TestMap(omm.Mapper):
            name = omm.MapField("test.name")
            age = omm.MapField("test.age", delete_value=True)
            sex = omm.MapField("test.sex")

        class DataCls(object):

            class DataSubCls(object):

                def __init__(self):
                    self.name = "Test Example"
                    self.age = 23
                    self.sex = "test"

            def __init__(self):
                self.test = self.DataSubCls()

        self.cls = TestMap
        self.data_cls = DataCls
        self.data = DataCls()
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_field_deletion(self):
        """The value should be delete."""
        self.assertNotIn("age", self.mapper.fields)
        self.assertNotIn("age", self.mapper.__dict__)

    def test_attr_access(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            self.data.test.age


class MapperDeletionValueFromFieldExceptionTest(TestCase):
    """Error Test due to field vlaue deletion."""

    def setUp(self):
        """Setup."""
        class TestMap(omm.Mapper):
            name = omm.MapField("test.name")
            age = omm.MapField("test.age", delete_value=True)
            sex = omm.MapField("test.sex")

        class DataCls(object):

            class DataSubCls(object):

                def __init__(self):
                    self.name = "Test Example"
                    self.sex = "test"

            def __init__(self):
                self.test = self.DataSubCls()

        self.cls = TestMap
        self.data_cls = DataCls
        self.data = DataCls()
        self.mapper = self.cls(self.data)
        del self.mapper.age

    def test_field_deletion(self):
        """It raises nothing."""
        self.assertNotIn("age", self.mapper.fields)
        self.assertNotIn("age", self.mapper.__dict__)

    def test_data_value(self):
        """The attribute shouldn't exist."""
        with self.assertRaises(AttributeError):
            self.data.test.age
