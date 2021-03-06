#!/usr/bin/env python
# coding=utf-8

"""Model Base."""

import collections as col
import json
import re
from functools import partial

import six

from .fields import FieldBase
from .helper import reduce_with_index
from .structures import ConDict


class MetaMapper(type):
    """The meta class of Mapper."""

    def __init__(self, name, bases, members):
        """Init."""
        self._fields = {}
        for (key, value) in members.items():
            if isinstance(value, FieldBase):
                self._fields[key] = value
        super(MetaMapper, self).__init__(name, bases, members)


class Mapper(six.with_metaclass(MetaMapper)):
    """
    Mapper Base Classs.

    Every class that uses this mapper should inherit this class.

    Useful Attributes:
        asdict: Set True if you put value as dict. By default, this value is
            Falsy value that means "put value as attribute."

    Use of asdict:
        Suppose that there is a mapper like this:
        ```Python
        class Test(Mapper):
            test = MapField("test.a.b.c")
        ```
        Then, putting the value "this is a test" there, you can get an instance
        of object via connected_object property, like this:
        ```Python
        class B(object):
            def __init__(self, c):
                self.c = c

        class A(object):
            def __init__(self):
                self.b = B("this is a test")

        class Test(object):
            def __init__(self):
                self.a = A()

        # connected_object = Test()
        ```
        However, setting self.asdict = True, connected_object become
        multi-dimentional dict like this:
        ```Python
        connected_object = {"test": {"a": {"b": {"c": "this is a test"}}}}
        ```
    """

    def __init__(self, target=None, **kwargs):
        """
        Initialize the object.

        Parameters:
            target: The target object. By default, None is set.
            **kwargs: Any attributes or meta-data.

        """
        if target is not None:
            self.connect(target)
        for (attr, value) in kwargs.items():
            setattr(self, attr, value)
        super(Mapper, self).__init__()

    def validate(self):
        """Validate the model."""
        self.__errors = {}
        self.__list = partial(sorted, key=tuple(self.fields.items()).index) \
            if getattr(self, "$testing$", False) else tuple
        rest_fields = self.__validate_each_field()
        rest_fields = self.__validate_consistency(rest_fields)
        return not bool(self.__errors)

    def __validate_each_field(self):
        """Validate each field."""
        fields = self.fields.items()
        error_fields = []
        for (name, field) in fields:
            try:
                field.validate()
            except ValueError as e:
                error_fields.append((name, field))
                self._register_error(name, str(e))
        return self.__list(set(fields) - set(error_fields))

    def _register_error(self, fldname, err):
        """
        Register an error message.

        Parameters:
            fldname: The name of the field.
            err: The message

        """
        if isinstance(self.__errors.get(fldname), list):
            self.__errors[fldname].append(err)
        else:
            self.__errors[fldname] = [err]

    def __validate_consistency(self, fields=None):
        """Check consistency of the class."""
        fields = [
            field for field in fields or self.fields.items()
            if isinstance(getattr(field[1], "set_cast", None), list)
        ]
        error_fields = []
        if not fields:
            return {}
        AttributeInfo = type("__AttrInfo__", (object, ), {})
        root = AttributeInfo()
        setattr(root, "$$type$$", fields[0][1].set_cast[0])
        setattr(root, "$$source$$", fields[0][0])
        err_msg = (
            "This field partially references the same path of {source}, "
            "but set_cast corresponding to \"{fldname}\" is not the same."
        )
        parse_pattern = re.compile(r"([^\.\[\]0-9]+)|\[([0-9]+)\]+")

        def check_consistency_for_each_value(cur, attr, index,
                                             attrs, name, field):
            attr_set_cast = field.set_cast[index + 1]
            current_target_str = ("(root).{}").format(
                (".").join(attrs[:index + 1])
            )
            current = cur
            try:
                current = getattr(current, attr)
                current_type = getattr(current, "$$type$$", None)
                err = err_msg.format(
                    source=getattr(current, "$$source$$", None),
                    fldname=current_target_str
                )
                if current_type is not attr_set_cast:
                    error_fields.append((name, field))
                    self._register_error(name, err)
            except AttributeError:
                setattr(current, attr, AttributeInfo())
                current = getattr(current, attr)
                setattr(
                    current, "$$type$$",
                    field.set_cast[index + 1]
                )
                setattr(current, "$$source$$", name)
            return current

        for (name, field) in fields:
            parsed_attrs = [
                el for pa in parse_pattern.findall(field.target)
                for el in pa if el
            ]
            current = root
            current_type = getattr(current, "$$type$$", None)
            err = err_msg.format(
                source=getattr(current, "$$source$$", None),
                fldname="(root)"
            )
            root_set_cast = field.set_cast[0]
            if current_type is not root_set_cast:
                error_fields.append((name, field))
                self._register_error(name, err)
            reduce_with_index(
                check_consistency_for_each_value, parsed_attrs, current,
                attrs=parsed_attrs, name=name, field=field
            )
        return self.__list(set(fields) - set(error_fields))

    @property
    def errors(self):
        """
        Return error-dict.

        The format of this property is compatible with [WTForms]. For example,
        if there are errors, this property returns a dict like this:

        ```JSON
        {
            "age": [
                "This field refernces partially the same path of name"
            ]
        }
        ```

        If there aren't any errors, None is returned.

        [WTForms]: https://wtforms.readthedocs.io/en/latest/
        """
        try:
            return self.__errors
        except AttributeError:
            raise NotImplementedError("Execute validate method first.")

    @property
    def connected_object(self):
        """Get connected object."""
        return getattr(self, "_target", None)

    def connect(self, target):
        """
        Connect the object/dict to the mapper.

        Parameters:
            target: The target object.

        """
        self._target = target
        if isinstance(target, ConDict):
            self._target.assign(self)

    @staticmethod
    def __extend_exclusion(fld, exclude_type, ser_type):
        exclude = getattr(fld, "exclude", None)
        exclude_method = getattr(fld, ("exclude_{}").format(ser_type), None)

        if any([
            not (exclude or exclude_method is None),
            exclude_method is True, exclude_method is False
        ]):
            exclude = exclude_method

        if isinstance(exclude, dict):
            if isinstance(exclude_method, dict) and \
                    exclude is not exclude_method:
                exclude.update(exclude_method)
            exclude = exclude.get(exclude_type, False)
        return exclude

    def __compose_dict(self, priority_list, exclude_type):
        dct = {}
        for (name, fld) in self.fields.items():
            if self.__extend_exclusion(fld, exclude_type, "serialize"):
                continue
            try:
                value = getattr(self, name)
                found_ser_fn = False
                for (loads, dumps) in priority_list:
                    try:
                        dct[name] = loads(getattr(value, dumps)()) if loads\
                            else getattr(value, dumps)()
                        found_ser_fn = True
                        break
                    except AttributeError:
                        continue
                if not found_ser_fn:
                    dct[name] = value
            except AttributeError:
                pass
        return dct

    @classmethod
    def __restore_dict(cls, dct, attr_call_list, exclude_type):
        ret = cls()
        for (name, value) in dct.items():
            fld = cls._fields.get(name)
            if fld:
                if cls.__extend_exclusion(fld, exclude_type, "deserialize"):
                    continue
                try:
                    set_cast = fld.set_cast
                    found_desr_fn = False
                    if isinstance(set_cast, list):
                        set_cast = set_cast[-1]
                    for (loads_attr, dumps_fn) in attr_call_list:
                        try:
                            setattr(
                                ret, name, getattr(
                                    set_cast, loads_attr
                                )(
                                    dumps_fn({name: value})
                                    if dumps_fn else
                                    {name: value}
                                )
                            )
                            found_desr_fn = True
                            break
                        except AttributeError:
                            continue
                    if not found_desr_fn:
                        raise AttributeError()
                except AttributeError:
                    setattr(ret, name, value)
        return ret

    def to_dict(self, exclude_type="dict"):
        """Convert the schema into dict."""
        return self.__compose_dict([(None, "to_dict")], exclude_type)

    @classmethod
    def from_dict(cls, dct, exclude_type="dict"):
        """
        Convert the given dict into the schema.

        Parameters:
            dct: The dict to be deserialize.

        """
        return cls.__restore_dict(dct, [("from_dict", None)], exclude_type)

    def dumps(self, ser_fn, exclude_type="custom"):
        """
        Serialize the map with specified function.

        Parameters:
            ser_fn: Serializatoin Function.
            exclude_type: The type of exclusion.

        """
        return ser_fn(self.to_dict(exclude_type))

    @classmethod
    def loads(self, desr_fn, data, exclude_type="custom"):
        """Deserialize the map with specified function."""
        return self.from_dict(desr_fn(data), exclude_type)

    def to_json(self, **kwargs):
        """
        Generate JSON string.

        Parameters:
            **kwargs: Any keyword arguemnt to be passed to json.dumps

        """
        return json.dumps(self.__compose_dict([
            (json.loads, "to_json"), (None, "to_dict")
        ], "json"))

    @classmethod
    def from_json(cls, json_str, **kwargs):
        """
        De-serialize JSON string into the object.

        Parameters:
            json_str: JSON string to be deserialized
            **kwargs: Any keyword arguments to be passed to json.loads

        """
        return cls.__restore_dict(
            json.loads(json_str, **kwargs),
            [("from_json", json.dumps), ("from_dict", None)],
            "json"
        )

    @property
    def fields(self):
        """Return fields."""
        (FieldList, FieldDict) = (
            partial(sorted, key=lambda cmp: cmp[0]), col.OrderedDict
        ) if getattr(self, "$testing$", False) else (list, dict)
        return FieldDict(FieldList(self._fields.items()))
