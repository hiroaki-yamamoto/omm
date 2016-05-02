#!/usr/bin/env python
# coding=utf-8


"""Mapper test case."""

import unittest

from omm import Mapper


class MapperConnectivityTest(unittest.TestCase):
    """Test case for mapper initialization test."""

    def setUp(self):
        """Setup the class."""
        class TestClass(object):
            pass
        self.TestClass = TestClass
        self.test_class = self.TestClass()

    def test_mapper_init(self):
        """Mapper can connect when initialized."""
        result = type("Generated Mapper", (Mapper, ), {})(self.test_class)
        self.assertIsInstance(result.connected_object, self.TestClass)


class MapperLazyConnectivityTest(unittest.TestCase):
    """Test case for mapper init test."""

    def setUp(self):
        """Setup the class."""
        self.TestClass = type("TestClass", (object, ), {})
        self.test_class = self.TestClass()

    def test_lazy_connect(self):
        """Lazy connection should work."""
        mapper = type("TestMap", (Mapper, ), {})()
        mapper.connect(self.test_class)
        self.assertIs(mapper.connected_object, self.test_class)
