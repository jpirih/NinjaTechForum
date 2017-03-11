#!/usr/bin/env python

import webapp2
from handlers.base import MainHandler, AboutHandler, CookiesAlertHandler
from handlers.topics import CreateTopicHandler, TopicDetailsHandler, DeleteTopicHandler
from handlers.users import UserLoginHandler, UserProfileHandler
from handlers.comments import CreateCommentHandler
from workers.email_comment_worker import EmailNewCommentWorker


app = webapp2.WSGIApplication([
    # base routes
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookiesAlertHandler, name="set-cookie"),

    # topics routes
    webapp2.Route('/topic/add', CreateTopicHandler, name="add-topic"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler, name="topic-delete"),
    webapp2.Route('/topic/<topic_id:\d+>/new-comment', CreateCommentHandler, name="create-comment"),

    # users routes
    webapp2.Route('/login', UserLoginHandler, name="user-login"),
    webapp2.Route('/user/<user_id:\d+>', UserProfileHandler, name="user-profile"),

    # tasks
    webapp2.Route("/task/email-new-comment", EmailNewCommentWorker, name="email-comment"),
], debug=True)
