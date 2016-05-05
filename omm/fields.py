#!/usr/bin/env python
# coding=utf-8

"""Fields."""

import re
from functools import reduce


class MapField(object):
    """Normal Map Field."""

    __index_find_pattern__ = re.compile("\[([0-9])+\]+")

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

        def lookup(data, attr):
            index = [
                int(value)
                for value in self.__index_find_pattern__.findall(attr)
            ]
            result = data[
                self.__index_find_pattern__.sub("", attr)
            ] if isinstance(data, dict) else getattr(
                data, self.__index_find_pattern__.sub("", attr)
            )
            if index:
                result = reduce(lambda v, i: v[i], index, result)
            return result
        return reduce(lookup, attrs, data)

    def __set__(self, obj, value):
        """Set descriptor."""
        asdict = getattr(obj, "asdict", False)
        GeneratedObject = type("GeneratedObject", (object, ), {})

        def get_or_create(target, attr):
            # indexes = [
            #     int(value)
            #     for value in self.__index_find_pattern__.findall(attr)
            # ]
            attr = self.__index_find_pattern__.sub("", attr)
            try:
                result = target[attr] if asdict else getattr(target, attr)
                return result
            except AttributeError:
                setattr(target, attr, GeneratedObject())
                return getattr(target, attr)
            except KeyError:
                target[attr] = {}
                return target[attr]

        if not obj.connected_object:
            obj.connect({} if asdict else GeneratedObject())
        attrs = self.target.split(".")
        # last_indexes = [
        #     int(value)
        #     for value in self.__index_find_pattern__.findall(attrs[-1])
        # ]
        last_attr = self.__index_find_pattern__.sub("", attrs[-1])
        target_obj = reduce(
            get_or_create, attrs[:-1], obj.connected_object
        )
        if asdict:
            target_obj[last_attr] = value
        else:
            setattr(target_obj, last_attr, value)

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
