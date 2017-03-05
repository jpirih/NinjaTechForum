#!/usr/bin/env python

import webapp2
from handlers.base import MainHandler, AboutHandler, CookiesAlertHandler
from handlers.topics import CreateTopicHandler, TopicDetailsHandler
from handlers.users import UserLoginHandler, UserProfileHandler


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookiesAlertHandler, name="set-cookie"),
    webapp2.Route('/topic/add', CreateTopicHandler, name="add-topic"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name="topic-details"),
    webapp2.Route('/login', UserLoginHandler, name="user-login"),
    webapp2.Route('/user/<user_id:\d+>', UserProfileHandler, name="user-profile"),
], debug=True)
