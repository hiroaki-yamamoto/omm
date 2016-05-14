#!/usr/bin/env python
# coding=utf-8

"""Mapping data for integration tests."""

import omm


class SimpleTestMapper(omm.Mapper):
    """Simple mapper."""

    name = omm.MapField("test.name")
    age = omm.MapField("test.age")
    sex = omm.MapField("test.sex")

    @staticmethod
    def generate_test_data(type_dict=False):
        """
        Generate test data.

        Parameters:
            type_dict: Set True if the data is expected to be typed as dict.
        """
        User = type("User", (object, ), {
            "name": "Test Example",
            "age": 960,
            "sex": None
        })
        gen_obj = type("GenObj", (object, ), {
            "test": User()
        })()

        return {
            "test": {
                "name": gen_obj.test.name,
                "age": gen_obj.test.age,
                "sex": gen_obj.test.sex
            }
        } if type_dict else gen_obj


class SimpleTestSchemaWithSimpleCast(omm.Mapper):
    """Simple Test Data with casting."""

    name = omm.MapField("test.user.name", set_cast=str)
    age = omm.MapField("test.user.age", get_cast=int)

    @staticmethod
    def generate_test_data(asdict=False):
        """Generate test data."""
        class User(object):
            def __init__(self):
                self.name = "Test Example"
                self.age = "199"

            def to_dict(self):
                return {"name": self.name, "age": self.age}

        class Test(object):
            def __init__(self):
                self.user = User()

            def to_dict(self):
                return {"user": self.user.to_dict()}

        class DataClass(object):
            def __init__(self):
                self.test = Test()

            def to_dict(self):
                return {"test": self.test.to_dict()}

        test = DataClass()
        return test.to_dict() if asdict else test


class SimpleTestSchemaWithComplexCast1(omm.Mapper):
    """Object based test mapper with complex casting."""

    TestObj1 = type("TestObj1", (object, ), {})
    TestObj2 = type("TestObj2", (object, ), {})
    name = omm.MapField(
        "test.user.name",
        set_cast=[TestObj1, dict, TestObj2, str]
    )


class SimpleTestSchemaWithComplexCast2(omm.Mapper):
    """Object based test mapper with complex casting."""

    GeneratedObject = type("GeneratedObject", (object, ), {})
    name = omm.MapField(
        "test.user.name",
        set_cast=[dict, GeneratedObject, dict, str]
    )


class DictSimpleTestSchema(SimpleTestMapper):
    """Dict-based test mapper."""

    asdict = True


class DictSimpleTestSchemaWithSimpleCast(SimpleTestSchemaWithSimpleCast):
    """Dict-based test mapper."""

    asdict = True


class DictSimpleTestSchemaWithComplexCast1(SimpleTestSchemaWithComplexCast1):
    """Dict-based test mapper."""

    asdict = True


class DictSimpleTestSchemaWithComplexCast2(SimpleTestSchemaWithComplexCast2):
    """Dict-based test mapper."""

    asdict = True


class ArrayMapTestSchema(omm.Mapper):
    """Array Mapper."""

    array = omm.MapField("test.array[1][1].correct")
    last_array = omm.MapField("test.array[1][2]")

    @staticmethod
    def generate_test_data(type_dict=False):
        """
        Generate test data.

        Parameters:
            type_dict: Set True if the data is expected to be typed as dict.
        """
        class ObjectClass(object):

            class Test(object):

                class ArrayElement(object):

                    def __init__(self, correct):
                        self.correct = correct

                def __init__(self):
                    self.array = [
                        [
                            type(self).ArrayElement(False),
                            type(self).ArrayElement(False)
                        ], [
                            type(self).ArrayElement(False),
                            type(self).ArrayElement(True),
                            "Hello World"
                        ]
                    ]

            def __init__(self):
                self.test = type(self).Test()
        return {
            "test": {"array": [
                [{"correct": False}, {"correct": False}],
                [{"correct": False}, {"correct": True}, "Hello World"],
            ]}
        } if type_dict else ObjectClass()


class ArrayMapCastingTestSchema(omm.Mapper):
    """Array mapper test data with casting."""

    name = omm.MapField("users[1][1].name", set_cast=str)
    age = omm.MapField("users[1][1].age", get_cast=int)
    lastest_score = omm.MapField("users[1][1].scores[3]", get_cast=int)

    @staticmethod
    def generate_test_data(asdict=False):
        """Generate test data."""
        class NameAge(object):
            def __init__(self, name, age, scores):
                self.name = name
                self.age = age
                self.scores = scores

            def to_dict(self):
                return {
                    "name": self.name,
                    "age": self.age,
                    "scores": self.scores
                }

        class Users(object):
            def __init__(self):
                self.users = [
                    None,
                    [None, NameAge("test", "119", ["g", "gk", "gi", "10"])]
                ]

            def to_dict(self):
                return {"users": [None, [None, self.users[1][1].to_dict()]]}
        users = Users()
        return users.to_dict() if asdict else users


class ArrayMapComplexCastingTestSchema(omm.Mapper):
    """Array map test casting schema (complex version)."""

    StartObj = type("StartObj", (object, ), {})
    Users = type("Users", (list, ), {})
    UserProfiles = type("UserProfiles", (list, ), {})
    Profile = type("Profile", (object, ), {})
    TestObj = type("TestObj", (object, ), {})
    InfoObj = type("InfoObj", (dict, ), {})

    name = omm.MapField(
        "test.users[0][1].info.name",
        set_cast=[
            StartObj, TestObj, Users, UserProfiles, Profile, InfoObj, str
        ]
    )


class ArrayMapDictTestSchema(ArrayMapTestSchema):
    """Array mapper (asdict)."""

    asdict = True


class ArrayMapDictCastingTestSchema(ArrayMapCastingTestSchema):
    """Array mapper (asdict)."""

    asdict = True
