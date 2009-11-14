from sqlalchemy import *
import meta, user
import hashlib
from datetime import datetime

bayes_feed_settings_table = Table('bayes_feed_settings', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('report_offset', Integer),
    Column('summarize_at', String(30)),
    UniqueConstraint('feed_id', 'user_id')
)

class BayesFeedSetting(object):
    def __init__(self):
        self.name = 'BayesFeedSetting'

    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return u"<BayesFeedSetting(%s)>" % self.id


