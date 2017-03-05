from google.appengine.ext import ndb


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    nickname = ndb.StringProperty()
    birth_date = ndb.StringProperty()
    admin = ndb.BooleanProperty(default=False)
    activated = ndb.BooleanProperty(default=False)

    @classmethod
    def get_or_create(cls, email, nickname):
        user = User.query(User.email == email).get()

        if not user:
            user = User(email=email, nickname=nickname)
            user.put()

        return user
