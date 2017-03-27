import webapp2
from handlers.comments import CreateCommentHandler, DeleteCommentHandler, EditCommentHandler, ReloadCommentHandler, \
    DestroyCommentHandler, DeletedCommentsListHandler
from handlers.topics import TopicDetailsHandler
from main import MainHandler
from models.comment import Comment

from models.topic import Topic
from models.user import User
from tests.helpers import BaseTest


class MainPageTests(BaseTest):
    app = webapp2.WSGIApplication(
        [
            webapp2.Route('/', MainHandler, name="main-page"),
            webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
            webapp2.Route('/topic/<topic_id:\d+>/new-comment', CreateCommentHandler, name="create-comment"),
            webapp2.Route('/comment/<comment_id:\d+>/delete', DeleteCommentHandler, name="comment-delete"),
            webapp2.Route('/comment/<comment_id:\d+>/edit', EditCommentHandler, name="comment-edit"),
            webapp2.Route('/comment/<comment_id:\d+>/reload', ReloadCommentHandler, name="comment-reload"),
            webapp2.Route('/comment/<comment_id:\d+>/destroy', DestroyCommentHandler, name="comment-destroy"),
            webapp2.Route('/comments-deleted-list', DeletedCommentsListHandler, name="deleted-comments-list"),
        ])

    def test_create_comment_handler_post(self):
        # create test user
        user = self.create_fake_admin()
        # get test user
        user_get = user.query().get()
        self.assertTrue(user_get)

        # create test topic
        topic = self.create_fake_topic()
        topic_get = Topic.query().get()
        self.assertTrue(topic_get)

        # csrf_token test
        csrf_token = self.create_fake_fake_token()
        content = "This is test comment"
        params = {"content": content, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/{}/new-comment'.format(topic.key.id()), params=params)
        # check if comment was created
        comment_get = Comment.query().get()
        self.assertIsNotNone(comment_get)

        self.assertEqual(post.status_int, 302)

    # edit commment test
    def test_comment_edit_handler_post(self):
        comment = self.create_fake_comment()
        csrf_token = self.create_fake_fake_token()

        content = "updated comment content"
        params = {"content": content, "csrf_token": csrf_token}
        post = self.testapp.post("/comment/{}/edit".format(comment.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

    # comment soft delete test
    def test_comment_delete_handler_post(self):
        # create test csrf token
        csrf_token = self.create_fake_fake_token()

        # create test comment
        comment = self.create_fake_comment()
        comment_get = Comment.query().get()
        self.assertTrue(comment_get)
        params = {"csrf_token": csrf_token}
        # test post request
        post = self.testapp.post('/comment/{}/delete'.format(comment.key.id()), params=params)
        self.assertEqual(post.status_int, 302)
        # check if  comment.deleted == True
        self.assertTrue(comment_get.deleted)

    # comment reload test
    def test_comment_reload_handler_post(self):
        self.create_fake_admin()
        user_get = User.query().get()
        self.assertTrue(user_get)

        csrf_token = self.create_fake_fake_token()
        # test deleted comment to reload
        comment = self.create_fake_deleted_comment()
        comment_get = Comment.query().get()
        self.assertTrue(comment_get)

        params = {"csrf_token": csrf_token}
        post = self.testapp.post("/comment/{}/reload".format(comment.key.id()), params=params)

        self.assertFalse(comment_get.deleted)
        self.assertEqual(post.status_int, 302)

    # comment destroy test
    def test_comment_destroy_handler_post(self):
        self.create_fake_admin()
        user_get = User.query().get()
        self.assertTrue(user_get)

        csrf_token = self.create_fake_fake_token()
        # test deleted comment to destroyed
        comment = self.create_fake_deleted_comment()
        comment_get = Comment.query().get()
        self.assertTrue(comment_get)

        params = {"csrf_token": csrf_token}
        post = self.testapp.post("/comment/{}/destroy".format(comment.key.id()), params=params)
        # check if comment is really gone
        destroyed_comment = Comment.query().get()
        self.assertIsNone(destroyed_comment)
        self.assertEqual(post.status_int, 302)


    # comment deleted list test
    def test_comments_deleted_list_handler_get(self):
        user = self.create_fake_admin()
        user_get = User.query().get()
        self.assertTrue(user_get)
        self.assertTrue(user_get.admin)

        comment = self.create_fake_deleted_comment()
        get = self.testapp.get('/comments-deleted-list')
        self.assertEqual(get.status_int, 200)
        self.assertIn("List of Deleted Comments", get.body)
        self.assertIn(comment.content, get.body)









