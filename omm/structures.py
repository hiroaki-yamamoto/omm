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

    def __getitem__(self, name):
        """Get Item."""
        if isinstance(name, str):
            return self.data[name]
        elif isinstance(name, MapField):
            index = list(self.model.fields.values()).index(name)
            key = list(self.model.fields.keys())[index]
            return self[key]
        else:
            raise KeyError
