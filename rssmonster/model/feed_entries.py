from sqlalchemy import *
import meta
import hashlib
from datetime import datetime

feed_entries_table = Table('feed_entries', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id')),
    Column('uid', String(100)),
    Column('title', String(100)),
    Column('summary', String(255)),
    Column('link', String(255)),
)

class FeedEntry(object):
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


