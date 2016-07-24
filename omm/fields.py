#!/usr/bin/env python
# coding=utf-8

"""Fields."""

import re
from functools import reduce
from .helper import (
    reduce_with_index, shrink_list, delete_elem, safe_delete_array_elem
)


class FieldBase(object):
    """
    The base class of any fields.

    This shouldn't be used for end-use, but all OMM fields should
    inhert this base field.
    """

    pass


class MapField(FieldBase):
    """Normal Map Field."""

    __index_find_pattern__ = re.compile("\[([0-9])+\]+")
    __NotSpecifiedYet__ = type("__NotSpecifiedYet__", (object, ), {})
    __GeneratedObject__ = type("__GeneratedObject__", (object, ), {})

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
            clear_parent: clear the parent's value if this value is true and
                when __delete__ descriptor is called.
            exclude: Set True if you want to prevent
                serializatoin and deserialization from all
                type of method. If you want to prevent serialization and
                deserialization from specific type, set dict to this option.
                For example, the following code means "Exclude this field from
                serialization and deserialization if the types are json and
                msgpack." Btw, msgpack type can be defined by specifying
                `exclusion_type` at loads and dumps of the model.
                ```python
                MapField("test.obj", exclude={
                    "json": True,
                    "dict": False,
                    "custom": False,
                    "msgpack": True
                })
                ```
            exclude_serialize: Set True or the dict described above
                if you want to exclude this field from serialization.
            exclude_deserialize: Set True or the dict described above
                if you want to exclude this field from deserialization.
            sep_char: Seperation character. Note that this can be
                multiple characters. By default, the value is '.'
            (Other arguments): They are treated as meta-data.
        """
        super(MapField, self).__init__()
        self.target = target
        kwargs.setdefault("sep_char", ".")
        for (attr, value) in kwargs.items():
            setattr(self, attr, value)

    def __split_name_index(self, attr):
        index = [
            int(value)
            for value in self.__index_find_pattern__.findall(attr)
        ]
        name = self.__index_find_pattern__.sub("", attr)
        return (name, index)

    def __lookup(self, data, attr):
        (name, index) = self.__split_name_index(attr)
        result = data[name] if isinstance(data, dict) else getattr(data, name)
        if index:
            result = reduce(lambda v, i: v[i], index, result)
        return result

    def __get_connected_object(self, mapper_instance):
        from .structures import ConDict
        cobj = mapper_instance.connected_object
        return cobj[self] if isinstance(cobj, ConDict) else cobj

    def __get__(self, obj, cls=None):
        """Get descriptor."""
        if obj is None:
            # If the object is None, the field is referenced from class
            # definition. In this case, the field should return self.
            return self
        data = None
        try:
            data = self.__get_connected_object(obj)
        except KeyError:
            data = None
        attrs = self.target.split(self.sep_char)
        ret = reduce(self.__lookup, attrs, data)
        if hasattr(self, "get_cast") and not isinstance(ret, self.get_cast):
            ret = self.get_cast(ret)
        return ret

    def __delete_attr(self, target, target_route):
        try:
            obj = reduce(self.__lookup, target_route[:-1], target)
            parent_obj = reduce(self.__lookup, target_route[:-2], target)
            (name, index) = self.__split_name_index(target_route[-1])
            if index:
                parent_obj = obj
                obj = self.__lookup(obj, name)
                parent_obj = reduce(lambda v, i: v[i], index[:-2], obj)
                obj = reduce(lambda v, i: v[i], index[:-1], obj)

                safe_delete_array_elem(obj, index[-1])

                if getattr(self, "clear_parent", False):
                    is_empty = all(
                        [el is None for el in obj] +
                        [isinstance(parent_obj, list)]
                    )
                    if is_empty:
                        safe_delete_array_elem(parent_obj, index[-2])
                    shrink_list(parent_obj)
                    if not parent_obj:
                        self.__delete_attr(
                            target,
                            target_route[:-1] + [name]
                        )
            else:
                delete_elem(obj, target_route[-1])
                if getattr(self, "clear_parent", False):
                    is_empty = not(
                        bool(obj)
                        if isinstance(obj, dict) else
                        bool(obj.__dict__)
                    )
                    if all([is_empty, target_route[:-1]]):
                        self.__delete_attr(target, target_route[:-1])
        except (AttributeError, KeyError):
            return

    def __delete__(self, instance):
        """Delete descriptor."""
        target = self.__get_connected_object(instance)
        target_route = self.target.split(self.sep_char)
        self.__delete_attr(target, target_route)

    def _cast_type(self, index, default=__NotSpecifiedYet__, index_only=False):
        ret = None
        try:
            ret = self.set_cast[index]
        except TypeError as e:
            if index_only and default is self.__NotSpecifiedYet__:
                raise e
            ret = default if index_only or index >= 0 else self.set_cast
        except AttributeError as e:
            if default is self.__NotSpecifiedYet__:
                raise e
            ret = default
        return ret

    def __correct_value(self, target, indexes, value):
        result_value = value
        if hasattr(self, "set_cast"):
            cast = self._cast_type(-1, None)
            if not any([cast is None, type(result_value) is cast]):
                result_value = cast(result_value)
        return target if isinstance(target, list) \
            else [] if indexes else result_value

    def __allocate_array(self, asdict, target, attr, current_position,
                         indexes, value=None):
        point = target[attr] if isinstance(target, dict) \
            else getattr(target, attr)
        for (num, index) in enumerate(indexes):
            cast = self._cast_type(
                current_position + num + 2,
                dict if asdict else self.__GeneratedObject__, True
            )
            point.extend([None] * (index - len(point) + 1))
            point[index] = (
                value if value is not None else cast()
            ) if num + 1 == len(indexes) else point[index] if isinstance(
                point[index], list
            ) else cast() if issubclass(cast, list) else []
            point = point[index]
        return point

    def validate(self):
        """
        Validate the field.

        If the validation is failed, ValueError is raised.
        """
        attrs = self.target.split(self.sep_char)
        num_cast = len(attrs) + len(
            self.__index_find_pattern__.findall(self.target)
        ) + 1
        if isinstance(getattr(self, "set_cast", None), list) and \
                len(self.set_cast) != num_cast:
            raise ValueError(
                ("The number of set_cast must be {}, not {}").format(
                    num_cast, len(self.set_cast)
                )
            )

    def __set__(self, obj, value):
        """Set descriptor."""
        attrs = self.target.split(self.sep_char)
        self.validate()
        asdict = getattr(obj, "asdict", False)
        GeneratedObject = type("GeneratedObject", (object, ), {})

        def get_or_create(target_delay, attr, cur_pos):
            (target, delay) = target_delay
            indexes = [
                int(value)
                for value in self.__index_find_pattern__.findall(attr)
            ]
            actual_attr = self.__index_find_pattern__.sub("", attr)
            result = None
            try:
                result = self.__allocate_array(
                    asdict, target, actual_attr, cur_pos, indexes
                )
            except AttributeError:
                cast = self._cast_type(cur_pos + delay + 1, GeneratedObject)
                setattr(
                    target, actual_attr,
                    [] if indexes and not issubclass(cast, list) else cast()
                )
                result = self.__allocate_array(
                    asdict, target, actual_attr, cur_pos, indexes
                )
            except KeyError:
                cast = self._cast_type(cur_pos + delay + 1, dict)
                target[actual_attr] = [
                ] if indexes and not issubclass(cast, list) else cast()
                result = self.__allocate_array(
                    asdict, target, actual_attr, cur_pos, indexes
                )
            return (result, delay + len(indexes))

        try:
            if not self.__get_connected_object(obj):
                obj.connect(
                    self._cast_type(0, dict if asdict else GeneratedObject)()
                )
        except KeyError:
            index = list(obj.fields.values()).index(self)
            field_name = list(obj.fields.keys())[index]
            obj.connected_object[field_name] = self._cast_type(
                0, dict if asdict else GeneratedObject
            )()
        last_indexes = [
            int(index_str)
            for index_str in self.__index_find_pattern__.findall(attrs[-1])
        ]
        last_attr = self.__index_find_pattern__.sub("", attrs[-1])
        target_obj = reduce_with_index(
            get_or_create, attrs[:-1], (self.__get_connected_object(obj), 0)
        )[0]
        if isinstance(target_obj, dict):
            target_obj[last_attr] = self.__correct_value(
                target_obj.get(last_attr, None),
                last_indexes, value
            )
        else:
            setattr(
                target_obj, last_attr, self.__correct_value(
                    getattr(target_obj, last_attr, None),
                    last_indexes, value
                )
            )
        self.__allocate_array(
            asdict, target_obj, last_attr, -1, last_indexes, value
        )

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
