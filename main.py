#!/usr/bin/env python

import webapp2
from handlers.base import MainHandler, AboutHandler, CookiesAlertHandler


app=webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookiesAlertHandler, name="set-cookie"),
], debug=True)
