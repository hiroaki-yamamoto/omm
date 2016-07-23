#!/usr/bin/env python
# coding=utf-8

"""Data structures."""

from .fields import MapField

from six.moves import UserDict


class ConDict(UserDict):
    """Connection Dict for omm."""

    def assign(self, model):
        """
        Assign map.

        Paramters:
            model: An instance of Mapper class.

        Important Note: You shouldn't use this function for general purpose.
            This function is used for connecting map and this dict, but it
            doesn't Mapper.connect function. To call this function, use
            connect method of the mapper.
        """
        self.__model = model

    @property
    def model(self):
        """Return current model."""
        return self.__model

    def __iter__(self):
        """Return iterable."""
        return iter(self.data)

    def __getitem__(self, name):
        """Get Item."""
        key = name
        if isinstance(key, MapField):
            index = list(self.model.fields.values()).index(key)
            key = list(self.model.fields.keys())[index]
        return self.data[key]

    def __contains__(self, item):
        """Check if item exists."""
        key = item
        if isinstance(key, MapField):
            index = list(self.model.fields.values()).index(key)
            key = list(self.model.fields.keys())[index]
        return key in self.data
