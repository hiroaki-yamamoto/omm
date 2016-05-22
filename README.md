# Object Model Mapper

[![Build Status]][Build Status Link] [![Coverage Status]][Coverage Link]
[![Code Health]][Landscape Link]

[Coverage Status]: https://coveralls.io/repos/github/hiroaki-yamamoto/omm/badge.svg?branch=master
[Coverage Link]: https://coveralls.io/github/hiroaki-yamamoto/omm?branch=master
[Build Status]: https://travis-ci.org/hiroaki-yamamoto/omm.svg?branch=master
[Build Status Link]: https://travis-ci.org/hiroaki-yamamoto/omm
[Code Health]: https://landscape.io/github/hiroaki-yamamoto/omm/master/landscape.svg?style=flat
[Landscape Link]: https://landscape.io/github/hiroaki-yamamoto/omm/master


## What This?
This script bypasses models into other models. For example, you can flat
multi-depth model with this script, or you can make multi-depth model from
flat models.

## Why I Make This?
When I used MongoEngine, I needed to design the model like this:

```python
import mongoengine as db

class RecentPrevAmount(db.EmbeddedDocument):
  recent = db.FloatField()
  prev = db.FloatField()

class AssetInfo(db.Document):
  assets = db.EmbeddedDocumentField(RecentPrevAmount)
  cash = db.EmbeddedDocumentField(RecentPrevAmount)
  receivable = db.EmbeddedDocumentField(RecentPrevAmount)
  revenue = db.EmbeddedDocumentField(RecentPrevAmount)
  cogs = db.EmbeddedDocumentField(RecentPrevAmount)
```

And creating RestAPI in above order without "Undefiend property" error,
it is needed to create 5 curd resources:

* `[GET, POST, PUT, DELETE] /assets`
* `[GET, POST, PUT, DELETE] /cash`
* `[GET, POST, PUT, DELETE] /receivable`
* `[GET, POST, PUT, DELETE] /revenue`
* `[GET, POST, PUT, DELETE] /cogs`

For each resource, the text like following is output/input:
```JSON
{"recent": 10.0, "prev": 14.0}
```

This means, sending tons of requests is needed to file asset information and
it may have frontend slow. To avoid the problem, the number of request to send
should be reduced as far as possible. The ideal resource is one resource with
the following format:

```JSON
{
  "assets_recent": 10.0,
  "assets_prev": 11.0,
  "cash_recent": 12.0,
  "receivable_prev": 13.0,
  "revenue_recent": 14.0,
  "cogs_prev": 15.0
}
```

Of course, above is not good for public api
(On public api, recent and prev should be embedded in a field),
but above structure reduces the number of requests.

## How to use

I think you must need example code than the doc.

```Python
import mongoengine as db
import omm

# First, let's define the target models as usual.
class Address(db.EmbeddedDocument):
  street = db.ListField(db.StringField, required=True)
  city = db.StringField(required=True)
  state = db.StringField(required=True)
  country = db.StringField(required=True)

class User(db.Document):
  email = EmailField(primary_key=True)
  first_name = StringField(required=True)
  last_name = StringField(required=True)
  address = db.EmbeddedDocument(Address, required=True)

  @property
  def full_name(self):
    return (" ").join([self.first_name, self.last_name])

  @full_name.setter:
  def full_name(self, value):
    try:
      (self.first_name, self.last_name) = value.split(" ")
    except ValueError:
      pass

# Then, define the map.
class UserMapper(omm.Mapper):
  # Note that set_cast can be non-list, i.e. str. However, in this case,
  # we use User because the root object type is User.
  fullname = omm.MapField("full_name", set_cast=[User, str])
  email = omm.MapField("email", set_cast=[User, str])
  # For third element should be list or any class that inherits list because
  # the target is typed as list.
  street1 = omm.MapField(
    "address.street[0]", set_cast=[User, Address, list, str]
  )
  street2 = omm.MapField(
    "address.street[1]", set_cast=[User, Address, list, str]
  )
  city = omm.MapField("address.city", set_cast=[User, Address, str])
  state = omm.MapField("address.state", set_cast=[User, Address, str])
  country = omm.MapField("address.country", set_cast=[User, Address, str])

TODO
```

## License (MIT License)

Copyright (c) 2016 Hiroaki Yamamoto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
