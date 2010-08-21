#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run some bot jobs on GAE."""

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from opera.snapshot import CheckHandler, ParseFeedCheckHandler, DownloadHandler, UploadCheckHandler, CleanUpHandler
import logging

class NotFound(webapp.RequestHandler):
    def get(self):
        logging.info("%s requested %s." % (self.request.remote_addr, self.request.url))
        self.error(400)

def main():
    application = webapp.WSGIApplication(
        [
            (r'/opera/snapshot/check', CheckHandler),
            (r'/opera/snapshot/parsefeed', ParseFeedCheckHandler),
            (r'/opera/snapshot/download', DownloadHandler),
            (r'/opera/snapshot/upload', UploadCheckHandler),
            (r'/opera/snapshot/cleanup', CleanUpHandler),
            (r'/opera/.*', NotFound),
        ],
        debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
