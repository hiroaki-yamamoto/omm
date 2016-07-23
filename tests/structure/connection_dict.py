#!/usr/bin/env python
# coding=utf-8

"""Connection dict tests."""

from unittest import TestCase

from omm import ConDict

from ..mapdata import SimpleTestMapper


class TestData(TestCase):
    """The basis of the tests."""

    def setUp(self):
        """Setup."""
        class Value(object):

            def __init__(self, name, value):
                setattr(self, name, value)

        class Test(object):

            def __init__(self, obj):
                self.Test = obj

        self.value_cls = Value
        self.test_cls = Test

        self.name = {"test": {"name": "test"}}
        self.age = Test(Value("age", 29))
        self.dct = ConDict({
            "name": self.name,
            "age": self.age
        })


class DataTest(TestData):
    """The data of ConDict class test."""

    def check_data(self):
        """self.dct contains name and age as keys."""
        self.assertIn("name", self.dct)
        self.assertIn("age", self.dct)


class AssignTest(TestData):
    """assign function test."""

    def test_assign(self):
        """self.dct.map should be proper value after assign is called."""
        test = "Test"
        self.dct.assign(test)
        self.assertIs(self.dct.model, test)


class GetItemTest(TestData):
    """Item fetch test."""

    def setUp(self):
        """Setup."""
        super(GetItemTest, self).setUp()
        self.map_cls = SimpleTestMapper
        self.map = self.map_cls(self.dct)
        self.dct.assign(self.map)

    def test_getitem_by_name(self):
        """ConDict[name] should work properly."""
        self.assertIs(self.dct["name"], self.name)
        self.assertIs(self.dct["age"], self.age)
        with self.assertRaises(KeyError):
            print(self.dct["sex"])

    def test_getitem_by_field(self):
        """ConDict[field] should work properly."""
        name = self.map_cls.name
        age = self.map_cls.age
        sex = self.map_cls.sex
        self.assertIs(self.dct[name], self.name)
        self.assertIs(self.dct[age], self.age)
        with self.assertRaises(KeyError):
            print(self.dct[sex])

    def test_get_item_by_other(self):
        """CondDict[int] should raise KeyError."""
        with self.assertRaises(KeyError):
            print(self.dct[1])


class ItemContainsTest(TestData):
    """Item contains test."""

    def setUp(self):
        """Setup."""
        super(ItemContainsTest, self).setUp()
        self.map_cls = SimpleTestMapper
        self.map = self.map_cls(self.dct)
        self.dct.assign(self.map)

    def test_contains_by_name(self):
        """ConDict should contain name and age, but not cointans sex."""
        self.assertIn("name", self.dct)
        self.assertIn("age", self.dct)
        self.assertNotIn("sex", self.dct)

    def test_contains_by_field(self):
        """ConDict should/shouldn't contain proper fields."""
        name = self.map_cls.name
        age = self.map_cls.age
        sex = self.map_cls.sex
        self.assertIn(name, self.dct)
        self.assertIn(age, self.dct)
        self.assertNotIn(sex, self.dct)


class ItemIterationTest(TestData):
    """Item iteration test."""

    def setUp(self):
        """Setup."""
        super(ItemIterationTest, self).setUp()
        self.map_cls = SimpleTestMapper
        self.map = self.map_cls(self.dct)
        self.dct.assign(self.map)

    def test_iter_count(self):
        """len(map) should be proper."""
        self.assertEqual(len(self.dct), 2)

    def test_iter_list(self):
        """The generated list should be proper."""
        self.assertListEqual(
            [key for key in self.dct],
            [key for key in self.dct.data]
        )
