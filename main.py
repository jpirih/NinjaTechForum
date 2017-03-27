#!/usr/bin/env python

import webapp2

from crons.delete_topics import DeleteTopicCron
from crons.delete_comments import DeleteCommentsCron
from crons.newest_topics_cron import NewestTopicsCron
from handlers.base import MainHandler, AboutHandler, CookiesAlertHandler
from handlers.gallery import GalleryHandler
from handlers.topics import CreateTopicHandler, TopicDetailsHandler, DeleteTopicHandler, DeletedTopicsListHandler, \
    EditTopicHandler
from handlers.topics import ReloadTopicHandler, DestroyTopicHandler
from handlers.users import UserLoginHandler, UserProfileHandler
from handlers.comments import CreateCommentHandler, DeleteCommentHandler, EditCommentHandler, ReloadCommentHandler, \
    DestroyCommentHandler, DeletedCommentsListHandler
from handlers.subscriptions import SubscribeToNewTopics
from workers.email_comment_worker import EmailNewCommentWorker


app = webapp2.WSGIApplication([
    # base routes
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/gallery', GalleryHandler, name="gallery"),
    webapp2.Route('/set-cookie', CookiesAlertHandler, name="set-cookie"),

    # topics routes
    webapp2.Route('/topic/add', CreateTopicHandler, name="add-topic"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler, name="topic-delete"),
    webapp2.Route('/topic/<topic_id:\d+>/edit', EditTopicHandler, name="topic-edit"),
    webapp2.Route('/topic/<topic_id:\d+>/reload', ReloadTopicHandler, name="topic-reload"),
    webapp2.Route('/topic/<topic_id:\d+>/destroy', DestroyTopicHandler, name="topic-destroy"),
    webapp2.Route('/topics-deleted-list', DeletedTopicsListHandler, name="topic-deleted-list"),

    # comments routes
    webapp2.Route('/topic/<topic_id:\d+>/new-comment', CreateCommentHandler, name="create-comment"),
    webapp2.Route('/comment/<comment_id:\d+>/delete', DeleteCommentHandler , name="comment-delete"),
    webapp2.Route('/comment/<comment_id:\d+>/edit', EditCommentHandler , name="comment-edit"),
    webapp2.Route('/comment/<comment_id:\d+>/reload', ReloadCommentHandler , name="comment-reload"),
    webapp2.Route('/comment/<comment_id:\d+>/destroy', DestroyCommentHandler , name="comment-destroy"),
    webapp2.Route('/comments-deleted-list', DeletedCommentsListHandler , name="deleted-comments-list"),
    webapp2.Route('/subscribe/new-topics', SubscribeToNewTopics, name="subscribe-new-topics"),

    # users routes
    webapp2.Route('/login', UserLoginHandler, name="user-login"),
    webapp2.Route('/user/<user_id:\d+>', UserProfileHandler, name="user-profile"),

    # tasks
    webapp2.Route("/task/email-new-comment", EmailNewCommentWorker, name="email-comment"),

    # cron jobs
    webapp2.Route("/cron/delete-topics", DeleteTopicCron, name="cron-delete-topics"),
    webapp2.Route("/cron/delete-comments", DeleteCommentsCron, name="cron-delete-comments"),
    webapp2.Route("/cron/email-newest-topics", NewestTopicsCron, name="cron-newest-topics"),
], debug=True)
