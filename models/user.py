from google.appengine.ext import ndb
from google.appengine.api import users


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

    @classmethod
    def is_admin(cls, current_user):
        user = cls.query(cls.email == current_user.email).get()
        if user.admin:
            return True
        else:
            return False

    @classmethod
    def logged_in_user(cls):
        current_user = users.get_current_user()
        if current_user:
            user = cls.query(cls.email == current_user.email()).get()
            return user
        else:
            user = None
            return user

    @staticmethod
    def is_author(current_user, item):
        if current_user.email == item.author_email:
            return True
        else:
            return False




