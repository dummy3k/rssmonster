from sqlalchemy import *
import meta
import hashlib
from datetime import datetime

feeds_table = Table('feeds', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
    Column('url', String(255)),
    Column('last_update', DateTime),
)

class Feed(object):
    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    def __repr__(self):
        return "<Feed()>"
        #return "<Feed('%s', '%s')>" % (self.name, self.openid)

