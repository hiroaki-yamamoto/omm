#!/usr/bin/env python
# coding=utf-8

"""Fields."""

import re
from functools import reduce


class MapField(object):
    """Normal Map Field."""

    def __init__(self, target=None):
        """
        Initialize the class.

        Parameters:
            target: The field to bind. Not that you can bind child field by
                using dot-notation.
        """
        self.target = target

    def __get__(self, obj, cls=None):
        """Get descriptor."""
        if obj is None:
            # If the object is None, the field is referenced from class
            # definition. In this case, the field should return self.
            return self
        data = obj.connected_object
        attrs = self.target.split(".")
        index_find_pattern = re.compile("\[([0-9])+\]+")

        def lookup(data, attr):
            index = [
                int(value) for value in index_find_pattern.findall(attr)
            ]
            result = data[
                index_find_pattern.sub("", attr)
            ] if isinstance(data, dict) else getattr(
                data, index_find_pattern.sub("", attr)
            )
            if index:
                result = reduce(lambda v, i: v[i], index, result)
            return result
        return reduce(lookup, attrs, data)

    def __set__(self, obj, value):
        """Set descriptor."""
        GeneratedObject = type("GeneratedObject", (object, ), {})

        def get_or_create(target, attr):
            try:
                return getattr(target, attr)
            except AttributeError:
                setattr(target, attr, GeneratedObject())
                return getattr(target, attr)
        if not obj.connected_object:
            obj.connect(GeneratedObject())
        attrs = self.target.split(".")
        target_obj = reduce(
            get_or_create, attrs[:-1], obj.connected_object
        )
        setattr(target_obj, attrs[-1], value)

    @property
    def target(self):
        """Get the target field."""
        return getattr(self, "_target", None)

    @target.setter
    def target(self, value):
        """
        Set the target field.

        Parameters:
            value: The dot notated target.
        """
        self._target = value
