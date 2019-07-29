from google.appengine.ext import ndb

class Dog(ndb.Model):
    name = ndb.StringProperty()
    breed = ndb.StringProperty()
    gender = ndb.StringProperty()
    age = ndb.StringProperty()
    size = ndb.StringProperty()
    socialLevel = ndb.StringProperty()
    activityLevel = ndb.StringProperty()
    friendlyLevel = ndb.StringProperty()
    profilePic = ndb.BlobProperty()
    ownerName = ndb.StringProperty()

class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    dogs = ndb.KeyProperty(Dog, repeated=True)
    city = ndb.StringProperty()
    state = ndb.StringProperty()

