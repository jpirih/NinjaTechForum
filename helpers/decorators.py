from google.appengine.api import memcache, users


def validate_csrf(handler):
    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        csrf_token = self.request.get('csrf_token')
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or str(mem_token) != user.email():
            return self.write('You are hacker')
        else:
            return handler(self, *args, **kwargs)
    return wrapper
