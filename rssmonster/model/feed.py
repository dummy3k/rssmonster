from sqlalchemy import *
import meta
import hashlib
from datetime import datetime
from feed_entries import FeedEntry

feeds_table = Table('feeds', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
    Column('url', String(255)),
    Column('last_fetch', DateTime),
    Column('last_builddate', DateTime),
    Column('updated', DateTime),
    Column('subtitle', String(100)),
    Column('language', String(100)),
    Column('image', String(100)),
    Column('link', String(100)),
)

class Feed(object):
    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    def __repr__(self):
        return "<Feed()>"
        #return "<Feed('%s', '%s')>" % (self.name, self.openid)

    def get_entry_count(self):
        query = meta.Session.query(FeedEntry)
        return query.filter_by(feed_id=self.id).count()

    def get_entries(self):
        query = meta.Session.query(FeedEntry)
        return query.filter(FeedEntry.feed_id == self.id)
    