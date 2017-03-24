""" Helper  class for running tests """

import os
import unittest
import uuid

import webapp2
import webtest
from google.appengine.api import memcache

from google.appengine.ext import testbed
from main import MainHandler
from models.topic import Topic
from models.user import User


class BaseTest(unittest.TestCase):
    app = webapp2.WSGIApplication(
        [
            webapp2.Route('/', MainHandler, name="main-page"),
        ])
    def setUp(self):


        self.testapp = webtest.TestApp(self.app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        os.environ['USER_IS_ADMIN'] = '1'

    def create_fake_admin(self, first_name="Some", last_name="Some", email="some.user@example.com",
                          nickname="some.user", activated=True, admin=True):

        admin_user = User(first_name=first_name, last_name=last_name, email=email, nickname=nickname,
                          activated=activated, admin=admin)
        admin_user.put()

        return admin_user



    def create_fake_fake_token(self):
        csrf_token = str(uuid.uuid4())
        user = self.create_fake_admin()
        memcache.add(key=csrf_token, value=user.email, time=600)
        return csrf_token

    def create_fake_topic(self, title="New Test Topic", content="This is test.topic", author=None):

        if not author:
            test_author = self.create_fake_admin()
            topic = Topic.crate(title=title, content=content, author=test_author)
            return topic
        else:
            topic = Topic.crate(title=title, content=content, author=author)
            return topic

    def create_fake_topic_deleted(self, title="New Test Topic Deleted", content="This is test.topic", deleted=True):

        test_author = self.create_fake_admin()
        topic = Topic(title=title, content=content, author_email=test_author.email, deleted=True)
        topic.put()
        return topic


    def tearDown(self):
        self.testbed.deactivate()


