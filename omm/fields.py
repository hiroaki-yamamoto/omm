#!/usr/bin/env python
# coding=utf-8

"""Fields."""

import re
from functools import reduce


class MapField(object):
    """Normal Map Field."""

    __index_find_pattern__ = re.compile("\[([0-9])+\]+")

    def __init__(self, target=None, **kwargs):
        """
        Initialize the class.

        Parameters:
            target: The field to bind. Not that you can bind child field by
                using dot-notation.

        Keyword Arguments:
            set_cast: This is called when the value is set, and the value is
                casted into the type specified by this argument. This argument
                should be callable. By default, a class that inherits object
                is used.
            get_cast: This is called when getting the value, and the returned
                value is casted into the type specified by this argument.
                This argument should be callable.
            (Other arguments): They are treated as meta-data.
        """
        self.target = target
        for (attr, value) in kwargs.items():
            setattr(self, attr, value)

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

        def allocate_array(target, attr, indexes, value=None):
            point = target[attr] if asdict else getattr(target, attr)
            for (num, index) in enumerate(indexes):
                point.extend([None] * (index - len(point) + 1))
                point[index] = (
                    value if value is not None else {}
                    if asdict else GeneratedObject()
                ) if num + 1 == len(indexes) else point[index] if isinstance(
                    point[index], list
                ) else []
                point = point[index]
            return point

        def correct_value(target, indexes, value):
            return target if isinstance(target, list) \
                else [] if indexes else value

        def get_or_create(target, attr):
            indexes = [
                int(value)
                for value in self.__index_find_pattern__.findall(attr)
            ]
            actual_attr = self.__index_find_pattern__.sub("", attr)
            result = None
            try:
                result = allocate_array(target, actual_attr, indexes)
            except AttributeError:
                setattr(
                    target, actual_attr, [] if indexes else GeneratedObject()
                )
                result = allocate_array(target, actual_attr, indexes)
            except KeyError:
                target[actual_attr] = [] if indexes else {}
                result = allocate_array(target, actual_attr, indexes)
            return result

        if not obj.connected_object:
            obj.connect({} if asdict else GeneratedObject())
        attrs = self.target.split(".")
        last_indexes = [
            int(index_str)
            for index_str in self.__index_find_pattern__.findall(attrs[-1])
        ]
        last_attr = self.__index_find_pattern__.sub("", attrs[-1])
        target_obj = reduce(
            get_or_create, attrs[:-1], obj.connected_object
        )
        if asdict:
            target_obj[last_attr] = correct_value(
                target_obj.get(last_attr, None),
                last_indexes, value
            )
        else:
            setattr(
                target_obj, last_attr, correct_value(
                    getattr(target_obj, last_attr, None),
                    last_indexes, value
                )
            )
        allocate_array(target_obj, last_attr, last_indexes, value)

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
