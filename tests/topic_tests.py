import webapp2

from handlers.topics import CreateTopicHandler, TopicDetailsHandler, DeleteTopicHandler, ReloadTopicHandler, DestroyTopicHandler, \
    DeletedTopicsListHandler
from main import MainHandler
from tests.helpers import BaseTest


class TopicTests(BaseTest):
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

    # show page for creating new topic get test
    def test_add_topic_handler_get(self):
        get = self.testapp.get('/topic/add')  # get main handler
        self.assertEqual(get.status_int, 200)  # if GET request was ok, it should return 200 status code
        self.assertIn("Create New Topic", get.body)

    # create new topic post method test
    def test_add_topic_handler_post(self):
        # POST
        csrf_token = self.create_fake_fake_token()
        user = self.create_fake_admin()

        title = "Some new topic"
        text = "This is a new topic. Just for testing purposes."

        params = {"title": title, "content": text, "author_email": user.email, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/add', params)  # do a POST request
        self.assertEqual(post.status_int, 302)

    # get topic details handler
    def test_topic_details_handler_get(self):
        # GET
        topic = self.create_fake_topic()
        topic_id = topic.key.id()
        get = self.testapp.get('/topic/{}'.format(topic_id)) # do a GET request
        self.assertEqual(get.status_int, 200)
        self.assertIn("Add Comment", get.body)

    # topic soft delete test
    def test_topic_delete_handler_post(self):
        topic = self.create_fake_topic()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)

        csrf_token = self.create_fake_fake_token()

        params = {'csrf_token': csrf_token}
        post = self.testapp.post('/topic/{}/delete'.format(topic.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

        topic_deleted_get = topic.query().get()
        self.assertTrue(topic_deleted_get.deleted)

    # topic reload - by admin user
    def test_topic_reload_handler_post(self):
        # test user  with admin privileges
        csrf_token = self.create_fake_fake_token()
        user = self.create_fake_admin()

        user_get = user.query().get()
        self.assertTrue(user_get)

        topic = self.create_fake_topic_deleted()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)



        params = {"csrf_token": csrf_token}

        # runs post method
        post = self.testapp.post('/topic/{}/reload'.format(topic.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

        # check if deleted on test topic realy is False
        reloaded_topic_get = topic.query().get()
        self.assertFalse(reloaded_topic_get.deleted)


    # topic destroy by admin - deleted completly
    def test_topic_destroy_handler_post(self):
        # test user  with admin privileges
        user = self.create_fake_admin()

        user_get = user.query().get()
        self.assertTrue(user_get)

        topic = self.create_fake_topic_deleted()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)

        csrf_token =self.create_fake_fake_token()

        params = {"csrf_token": csrf_token}

        post = self.testapp.post('/topic/{}/destroy'.format(topic.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

        # check if current topic really does not exist anymore
        destroyed_topic_get = topic.query().get()
        self.assertIsNone(destroyed_topic_get)

    # check if admin can access the soft deleted topics list
    def test_topics_deleted_list_handler_get(self):
        # test user  with admin privileges
        user = self.create_fake_admin()
        user_get = user.query().get()
        self.assertTrue(user_get)

        topic = self.create_fake_topic_deleted()
        topic_get = topic.query().get()
        self.assertTrue(topic_get)

        get = self.testapp.get('/topics-deleted-list')
        self.assertEqual(get.status_int, 200)
        self.assertIn("List of Deleted topics", get.body)

