#!/usr/bin/env python
# coding=utf-8

"""Fields."""

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
        if isinstance(data, dict):
            def lookup_dict(data, attr):
                return data[attr]
            return reduce(lookup_dict, attrs, data)
        else:
            return reduce(getattr, attrs, data)

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
