from sqlalchemy import *
import meta
import hashlib
from datetime import datetime

import logging
log = logging.getLogger(__name__)

feed_entries_table = Table('feed_entries', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id')),
    Column('uid', String(100)),
    Column('title', String(100)),
    Column('summary', String(255)),
    Column('link', String(255)),
)

class FeedEntry(object):
    def __init__(self):
        log.debug("Hellllllo!")
        
    def __unicode__(self):
        return self.name

    def getHashedEmailAddress(self):
        if self.email:
            return hashlib.md5(self.email.strip().lower()).hexdigest()
        else:
            return hashlib.md5(self.openid.strip().lower()).hexdigest()
        
    __str__ = __unicode__

    def __repr__(self):
        return "<User()>"
        #return "<User('%s', '%s')>" % (self.name, self.openid)

    def actions(self, return_to):
        import rssmonster.lib.helpers as h
        return [
                {'link':h.url_for(controller='bayes', action='show_score', id=self.id, return_to=return_to),
                 'title':'Score'},
                {'link':h.url_for(controller='bayes', action='mark_as_spam', id=self.id, return_to=return_to),
                 'title':'Spam'},
                {'link':h.url_for(controller='bayes', action='mark_as_ham', id=self.id, return_to=return_to),
                 'title':'Ham'}
                 ]
        
