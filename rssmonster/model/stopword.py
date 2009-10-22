from sqlalchemy import *
import meta, user
import hashlib
from datetime import datetime
#from user import User
#from feed im

stopwords_table = Table('stopwords', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('word', String(50)),
)

class Stopword(object):
    def __init__(self):
        self.name = 'Stopword'
        
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return u"<Stopword(%s, %s, %s)>" % (self.user_id, self.feed_id, self.word)


