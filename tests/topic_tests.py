import os
import unittest
import uuid

import webapp2
import webtest
from google.appengine.api import memcache

from google.appengine.ext import testbed

from handlers.topics import CreateTopicHandler, TopicDetailsHandler, DeleteTopicHandler, ReloadTopic, DestroyTopic
from main import MainHandler
from models.topic import Topic


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', MainHandler, name="main-page"),
                webapp2.Route('/topic/add', CreateTopicHandler, name="add-topic"),
                webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
                webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler, name="topic-delete"),
                webapp2.Route('/topic/<topic_id:\d+>/reload', ReloadTopic, name="topic-reload"),
                webapp2.Route('/topic/<topic_id:\d+>/destroy', DestroyTopic, name="topic-destroy"),
            ])

        self.testapp = webtest.TestApp(app)
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
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_add_topic_handler(self):
        get = self.testapp.get('/topic/add')  # get main handler
        self.assertEqual(get.status_int, 200)  # if GET request was ok, it should return 200 status code
        self.assertIn("Create New Topic", get.body)

    def test_add_topic_post_handler(self):
        # POST
        csrf_token = str(uuid.uuid4())  # convert UUID to string
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        title = "Some new topic"
        text = "This is a new topic. Just for testing purposes."

        params = {"title": title, "content": text, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/add', params)  # do a POST request
        self.assertEqual(post.status_int,302)  # 302 means "redirect" - this is what we do at the end of POST method in TopicAdd handler

    def test_topic_details_handler(self):
        # GET
        topic = Topic(title="Another topic", content="Some text in the topic", author_email="some.user@example.com")
        topic.put()

        get = self.testapp.get('/topic/{}'.format(topic.key.id()))  # do a GET request
        self.assertEqual(get.status_int, 200)

