from google.appengine.ext import ndb


class Subscription(ndb.Model):
    email = ndb.StringProperty()

    subscribed = ndb.BooleanProperty(default=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, email):
        subscriber = cls(email=email)
        subscriber.put()
        return subscriber
