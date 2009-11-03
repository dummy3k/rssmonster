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
    Column('updated', DateTime),
)

class FeedEntry(object):
    def __init__(self):
        pass
                
    def __unicode__(self):
        return self.__repr__()

    def getHashedEmailAddress(self):
        if self.email:
            return hashlib.md5(self.email.strip().lower()).hexdigest()
        else:
            return hashlib.md5(self.openid.strip().lower()).hexdigest()
        
    __str__ = __unicode__

    def __repr__(self):
        return "<%s()>" % __name__

    def actions(self, return_to, user):
        import rssmonster.lib.helpers as h
        
        ret = [
                {'link':h.url_for(controller='/bayes', action='show_score', id=self.id),
                 'title':'Score'}
                ]
        
        from classification import Classification
        classy = meta.Session\
                .query(Classification)\
                .filter_by(user_id = user.id, entry_id=self.id).first()
        
        if not classy:
            ret.append({'title':'Spam', 'link':h.url_for(controller='/bayes', action='mark_as_spam', id=self.id, return_to=return_to)})
            ret.append({'title':'Ham', 'link':h.url_for(controller='/bayes', action='mark_as_ham', id=self.id, return_to=return_to)})
        elif classy.pool == 'spam':
            ret.append({'title':'Ham', 'link':h.url_for(controller='/bayes', action='mark_as_ham', id=self.id, return_to=return_to)})
        elif classy.pool == 'ham':
            ret.append({'title':'Spam', 'link':h.url_for(controller='/bayes', action='mark_as_spam', id=self.id, return_to=return_to)})
        else:
            raise "bad pool"
        
        return ret

    def mark_actions(self, return_to, user):
        import rssmonster.lib.helpers as h
        
        from classification import Classification
        classy = meta.Session\
                .query(Classification)\
                .filter_by(user_id = user.id, entry_id=self.id).first()
        
        if not classy:
            ret.append({'title':'Spam', 'link':h.url_for(controller='/bayes', action='mark_as_spam', id=self.id, return_to=return_to)})
            ret.append({'title':'Ham', 'link':h.url_for(controller='/bayes', action='mark_as_ham', id=self.id, return_to=return_to)})
        elif classy.pool == 'spam':
            ret.append({'title':'Ham', 'link':h.url_for(controller='/bayes', action='mark_as_ham', id=self.id, return_to=return_to)})
        elif classy.pool == 'ham':
            ret.append({'title':'Spam', 'link':h.url_for(controller='/bayes', action='mark_as_spam', id=self.id, return_to=return_to)})
        else:
            raise "bad pool"
        
        return ret

