#!/usr/bin/env python

"""Run some bot jobs on GAE."""

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<h1>It Works!</h1>')

def main():
    application = webapp.WSGIApplication(
        [
            (r'/', MainHandler),
        ],
        debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
