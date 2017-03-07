from google.appengine.api import users, memcache
from models.topic import Topic
from helpers.tools import DATE_TIME_FORMAT

import webapp2
import os
import jinja2
import uuid

from models.user import User

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        # cookies
        cookie = self.request.cookies.get("cookie_law")
        if cookie:
            params['cookies'] = True

        # google login
        user = users.get_current_user()
        if user:
            params['user'] = User.get_or_create(user.email(), user.nickname())
            params['logout_url'] = users.create_logout_url('/')
        else:
            params['login_url'] = users.create_login_url('/login')

        # Slo date time format
        params['slo_date'] = DATE_TIME_FORMAT

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

    def render_template_with_csrf(self, view_filename, params=None):
        if not params:
            params = {}

        # cookies
        cookie = self.request.cookies.get("cookie_law")
        if cookie:
            params['cookies'] = True

        # google login
        user = users.get_current_user()
        if user:
            params['user'] = User.get_or_create(user.email(), user.nickname())
            params['logout_url'] = users.create_logout_url('/')
        else:
            params['login_url'] = users.create_login_url('/login')

        # Slo date time format
        params['slo_date'] = DATE_TIME_FORMAT

        # csrf token
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=user.email(), time=3600)
        params['csrf_token'] = csrf_token

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        topics = Topic.query().order(-Topic.created_at).fetch()

        params = {'topics': topics}
        return self.render_template("base/main.html", params=params)


class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template('base/about.html')


class CookiesAlertHandler(BaseHandler):
    def post(self):
        self.response.set_cookie(key="cookie_law", value="accepted")
        return self.redirect_to("main-page")