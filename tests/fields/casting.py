#!/usr/bin/env python
# coding=utf-8

"""Mapfield casting unit test."""

import unittest as ut
import omm


class CastTypeTest(ut.TestCase):
    """MapField.__cast_type tests."""

    def setUp(self):
        """setUp function."""
        self.Objs = [
            type("Obj1", (object, ), {}),
            type("Obj2", (object, ), {}),
            type("Obj3", (object, ), {}),
            type("Obj4", (object, ), {})
        ]
        self.field = omm.MapField("test.name.aaaa")

    def test_normal_return(self):
        """Corresponding type should be returned."""
        import random as rd
        self.field.set_cast = self.Objs
        index = rd.randint(0, len(self.Objs) - 1)
        result = self.field._cast_type(index)
        self.assertIs(result, self.Objs[index])

    def test_type_error_normal(self):
        """self.Objs[0] should be returned."""
        self.field.set_cast = self.Objs[0]
        result = self.field._cast_type(-1)
        self.assertIs(result, self.Objs[0])

    def test_type_error_index_only(self):
        """Default type should be returned."""
        DefaultType = type("DefaultType", (object, ), {})
        self.field.set_cast = self.Objs[0]
        result = self.field._cast_type(0, DefaultType, True)
        self.assertIs(result, DefaultType)

    def test_type_error_raise(self):
        """TypeError should be raised."""
        self.field.set_cast = self.Objs[0]
        with self.assertRaises(TypeError):
            self.field._cast_type(0, index_only=True)

    def test_set_cast_not_set(self):
        """Default type should be returned."""
        DefaultType = type("DefaultType", (object, ), {})
        result = self.field._cast_type(0, DefaultType)
        self.assertIs(result, DefaultType)

    def test_set_cast_not_set_without_default_type(self):
        """AttributeError should be raised."""
        with self.assertRaises(AttributeError):
            self.field._cast_type(0)
