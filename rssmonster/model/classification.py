from sqlalchemy import *
import meta, user
import hashlib
from datetime import datetime
from feed_entries import FeedEntry

classifications_table = Table('classifications_entries', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('entry_id', Integer, ForeignKey('feed_entries.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('pool', String(5)),
)

class Classification(object):
    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    def __repr__(self):
        return "<Feed()>"
        #return "<Feed('%s', '%s')>" % (self.name, self.openid)


