#!/usr/bin/env python
# coding=utf-8

"""Exception for models."""


class FieldInconsistentError(TypeError):
    """
    Field inconsistent error.

    This error is raised when the model has fields that dont't have consistent
    casting types. For example, the following code is inconsistent and it
    causes this error:

    ```Python
    #!/usr/bin/env python
    # coding=utf-8
    # Note: This is **BAD** code
    import omm

    import models as db


    class InconsistentModel(omm.Model):
        name = omm.MapField(
            "test.user.name",
            set_cast=[db.StartObj, db.TestObj, db.UserObj, str]
        )
        alias = omm.MapField(
            "test.user.name",
            set_cast=[db.TestObj, db.UserObj, db.TestObj, int]
        )
        display_name = omm.MapField(
            "test.user.name",
            set_cast=[db.StartObj, db.UserObj, db.TestObj, str]
        )
    ```
    """

    pass
