from google.appengine.api import memcache, users
from functools import wraps
from models.user import User


def validate_csrf(handler):
    @wraps(handler)
    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        csrf_token = self.request.get('csrf_token')
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or str(mem_token) != user.email():
            return self.write('Csrf Token is not valid check if you are logged in')
        else:
            return handler(self, *args, **kwargs)
    return wrapper


def login_required(handler):
    @wraps(handler)
    def wrapper(self, *args, **kwargs):
        current_user = users.get_current_user()
        if not current_user:
            return self.redirect(users.create_login_url('/login'))
        user = User.get_or_create(email=current_user.email(), nickname=current_user.nickname())

        if user:
            return handler(self, *args, **kwargs)
        else:
            return self.redirect(users.create_login_url('/login'))

    return wrapper
