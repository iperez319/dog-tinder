from google.appengine.ext import ndb

class Dog(ndb.Model):
    name = ndb.StringProperty()
    breed = ndb.StringProperty()
    gender = ndb.StringProperty()
    age = ndb.StringProperty()
    size = ndb.StringProperty()
    socialLevel = ndb.StringProperty()
    activityLevel = ndb.StringProperty()
    profilePic = ndb.BlobProperty()
    ownerEmail = ndb.StringProperty()

class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    dogs = ndb.KeyProperty(Dog, repeated=True)
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    age = ndb.IntegerProperty()
    sex = ndb.StringProperty(choices=["Female", "Male", "Prefer not to say"])
    profilePic = ndb.BlobProperty()

