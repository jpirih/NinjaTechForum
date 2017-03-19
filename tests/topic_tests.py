import os
import unittest
import uuid

import webapp2
import webtest
from google.appengine.api import memcache

from google.appengine.ext import testbed

from handlers.topics import CreateTopicHandler, TopicDetailsHandler, DeleteTopicHandler, ReloadTopicHandler, DestroyTopicHandler, \
    DeletedTopicsListHandler
from main import MainHandler
from models.topic import Topic
from models.user import User


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', MainHandler, name="main-page"),
                webapp2.Route('/topic/add', CreateTopicHandler, name="add-topic"),
                webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
                webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler, name="topic-delete"),
                webapp2.Route('/topic/<topic_id:\d+>/reload', ReloadTopicHandler, name="topic-reload"),
                webapp2.Route('/topic/<topic_id:\d+>/destroy', DestroyTopicHandler, name="topic-destroy"),
                webapp2.Route('/topics-deleted-list', DeletedTopicsListHandler, name="topic-deleted-list"),
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
        os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    # show page for creating new topic get test
    def test_add_topic_handler_get(self):
        get = self.testapp.get('/topic/add')  # get main handler
        self.assertEqual(get.status_int, 200)  # if GET request was ok, it should return 200 status code
        self.assertIn("Create New Topic", get.body)

    # create new topic post method test
    def test_add_topic_handler_post(self):
        # POST
        csrf_token = str(uuid.uuid4())  # convert UUID to string
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        title = "Some new topic"
        text = "This is a new topic. Just for testing purposes."

        params = {"title": title, "content": text, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/add', params)  # do a POST request
        self.assertEqual(post.status_int,302)  # 302 means "redirect" - this is what we do at the end of POST method in TopicAdd handler

    # get topic details handler
    def test_topic_details_handler_get(self):
        # GET
        topic = Topic(title="Another topic", content="Some text in the topic", author_email="some.user@example.com")
        topic.put()

        get = self.testapp.get('/topic/{}'.format(topic.key.id()))  # do a GET request
        self.assertEqual(get.status_int, 200)
        self.assertIn("Add Comment", get.body)

    # topic soft delete test
    def test_topic_delete_handler_post(self):
        topic = Topic(title= "New test topic", content="Content of this topic", author_email='some.user@example.com')
        topic.put()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        params = {'csrf_token': csrf_token}
        post = self.testapp.post('/topic/{}/delete'.format(topic.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

        topic_deleted_get = Topic.query(Topic.deleted == True).get()
        self.assertTrue(topic_deleted_get)

    # topic reload - by admin user
    def test_topic_reload_handler_post(self):
        # test user  with admin privileges
        user = User(first_name="Test", last_name="User", email="some.user@example.com", nickname="some.user", activated=True, admin=True)
        user.put()

        user_get = user.query().get()
        self.assertTrue(user_get)

        topic = Topic(title= "Topic to reload", content="Some random content", author_email=user.email, deleted=True)
        topic.put()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value="some.user@example.com", time=600)

        params = {"csrf_token": csrf_token}

        # runs post method
        post = self.testapp.post('/topic/{}/reload'.format(topic.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

        # check if deleted on test topic realy is False
        reloaded_topic_get = Topic.query().get()
        self.assertFalse(reloaded_topic_get.deleted)


    # topic destroy by admin - deleted completly
    def test_topic_destroy_handler_post(self):
        # test user  with admin privileges
        user = User(first_name="Test", last_name="User", email="some.user@example.com", nickname="some.user",
                    activated=True, admin=True)
        user.put()

        user_get = user.query().get()
        self.assertTrue(user_get)

        topic = Topic(title="Topic to reload", content="Some random content", author_email=user.email, deleted=True)
        topic.put()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value="some.user@example.com", time=600)

        params = {"csrf_token": csrf_token}

        post = self.testapp.post('/topic/{}/destroy'.format(topic.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

        # check if current topic really does not exist anymore
        destroyed_topic_get = Topic.query().get()
        self.assertIsNone(destroyed_topic_get)

    # check if admin can access the soft deleted topics list
    def test_topics_deleted_list_handler_get(self):
        # test user  with admin privileges
        user = User(first_name="Test", last_name="User", email="some.user@example.com", nickname="some.user",
                    activated=True, admin=True)
        user.put()

        user_get = user.query().get()
        self.assertTrue(user_get)

        topic = Topic(title="Topic to reload", content="Some random content", author_email=user.email, deleted=True)
        topic.put()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)

        get = self.testapp.get('/topics-deleted-list')
        self.assertEqual(get.status_int, 200)
        self.assertIn("List of Deleted topics", get.body)
        self.assertIn(topic.title, get.body)

