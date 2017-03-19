import os
import unittest
import webapp2
import webtest
import uuid

from google.appengine.ext import testbed
from google.appengine.api import memcache

from handlers.comments import CreateCommentHandler, DeleteCommentHandler
from handlers.topics import TopicDetailsHandler
from main import MainHandler
from models.comment import Comment
from models.topic import Topic
from models.user import User


class MainPageTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', MainHandler, name="main-page"),
                webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
                webapp2.Route('/topic/<topic_id:\d+>/new-comment', CreateCommentHandler, name="create-comment"),
                webapp2.Route('/comment/<comment_id:\d+>/delete', DeleteCommentHandler, name="comment-delete"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_create_comment_handler_post(self):
        # create test user
        user = User(first_name="Test", last_name="User", email="some.user@example.com", nickname="some.user",
                    activated=True, admin=True)
        user.put()


        # get test user
        user_get = user.query().get()

        self.assertTrue(user_get)
        # create test topic
        topic = Topic(title= "Test Topic", content="This is another test Topic", author_email='some.user@example.com')
        topic.put()

        topic_get = Topic.query().get()
        self.assertTrue(topic_get)

        # csrf_token test
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        content = "This is test comment"
        params = {"content": content, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/{}/new-comment'.format(topic.key.id()), params=params)
        self.assertEqual(post.status_int, 302)


    def test_comment_delete_handler_post(self):
        # create test user
        user = User(first_name="Test", last_name="User", email="some.user@example.com", nickname="some.user",
                    activated=True, admin=True)
        user.put()

        # get test user
        user_get = user.query().get()
        self.assertTrue(user_get)

        # create test topic
        topic = Topic(title="Test Topic", content="This is another test Topic", author_email='some.user@example.com')
        topic.put()

        topic_get = Topic.query().get()
        self.assertTrue(topic_get)

        # csrf_token test
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        # create test comment

        content = "Test commment created only for deleting it"
        comment = Comment.create(content=content, user=user_get, topic=topic)

        comment_get = Comment.query().get()
        self.assertTrue(comment_get)

        # test post request
        post = self.testapp.post('/comment/{}/delete'.format(comment.key.id()))
        self.assertEqual(post.status_int, 302)

        # check if  comment.deleted == True
        self.assertTrue(comment_get.deleted)








