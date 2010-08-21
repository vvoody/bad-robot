#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch
import logging

class FeedStatus(db.Model):
    """Current content length of feed and how many times checked.

    One entity is enough, 'content_length' will be replaced by new value.
    """
    content_length = db.IntegerProperty(default=0)
    checked_times = db.IntegerProperty(default=0)

    @classmethod
    def rotate_checked_times(cls):
        """We will force to parse the feed if its content length has not
        changed in N(8) checked times. So we need to rotate it to zero.
        """
        k = FeedStatus.all().get()
        k.checked_times = 0
        k.put()

class Snapshots(db.Model):
    url = db.StringProperty()  # unique
    links = db.StringListProperty()  # real download files links
    status = db.StringProperty(default="notyet")  # 'downloading', 'downloaded', 'uploading', 'uploaded'
    token = db.StringProperty()  #
    confirmed = db.BooleanProperty(default=False)  # files really uploaded

# /opera/snapshot/check
class CheckHandler(webapp.RequestHandler):
    """Check whether the Content-Length of a rss feed altered. If
    changed or not changed in N checked times, we will re-parse the feed.

    Run every 15 mins. Skip next step 'downlaod' when the status of snapshot
    is 'downloading' or 'uploading'.
    """
    def get_feed_content_length(self):
        feed = "http://my.opera.com/desktopteam/xml/rss/blog/"
        result = urlfetch.fetch(feed, method='HEAD')
        return int(result.headers['content-length'])

    def has_job_doing(self):
        q = db.GqlQuery("SELECT * FROM Snapshots WHERE status in :1",
                        ["downloading", "uploading"])
        result = q.fetch(1)
        if result == []: return False
        return True

    def feed_checked_times(self):
        res = FeedStatus.all().get()
        return None if res is None else res.checked_times 

    def feed_changed(self):
        cl = self.get_feed_content_length()
        k = FeedStatus.all().get()
        if cl == k.content_length:
            k.checked_times += 1
            k.put()
            return False
        else:
            k.content_length = cl
            k.checked_times = 1
            k.put()
            return True
    
    def get(self):
        if self.has_job_doing() is True:
            logging.info("Certain job is doing, skip check.")
            return
        if self.feed_checked_times() == 8:
            FeedStatus.rotate_checked_times()
            logging.info("Feed not changed at 8 times, force to re-parse it.")
            self.response.out.write("/opera/Snapshots/parsefeed")
            return
        if self.feed_changed() is False:
            logging.info("Check done, feed not changed.")
            return
        else:
            self.response.out.write("/opera/Snapshots/parsefeed")

# /opera/snapshot/parsefeed
class ParseFeedCheckHandler(webapp.RequestHandler):
    pass

# /opera/snapshot/downlaod
class DownloadHandler(webapp.RequestHandler):
    pass

# /opera/snapshot/upload
class UploadCheckHandler(webapp.RequestHandler):
    pass

# /opera/snapshot/cleanup
class CleanUpHandler(webapp.RequestHandler):
    pass
