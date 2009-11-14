from sqlalchemy import *
import meta
import hashlib
from datetime import datetime

import logging
log = logging.getLogger(__name__)

users_table = Table('users', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('email', String(100)),
    Column('openid', String(255)),
    Column('banned', Boolean),
    Column('signup', DateTime),
    Column('last_login', DateTime),
)

class User(object):
    def __unicode__(self):
        return self.name

    def getHashedEmailAddress(self):
        if self.email:
            return hashlib.md5(self.email.strip().lower()).hexdigest()
        else:
            return hashlib.md5(self.openid.strip().lower()).hexdigest()

    def getDisplayName(self):
        if self.name:
            return self.name
        else:
            return "Unnamed User"

    __str__ = __unicode__

    def __repr__(self):
        return "<User()>"
        #return "<User('%s', '%s')>" % (self.name, self.openid)

    def updatelastlogin(self):
        self.last_login = datetime.now()

    def allow_edit(self, some_thing):
        if not some_thing:
            raise Exception('something isnt anything')

#        if type(some_thing) is Statement:
#            return (some_thing.userid == self.id)

        raise Exception('unknown type "%s"' % some_thing)

    def get_bayes_feed_setting(self, feed_id):
        log.info("feed_id: %s" % feed_id)
        log.info("self.bayes_feed_settings: %s" % self.bayes_feed_settings)
        for s in self.bayes_feed_settings:
            if int(s.feed_id) == int(feed_id):
                log.info("self.bayes_feed_settings: %s" % self.bayes_feed_settings)
                return s

        from bayes_feed_setting import BayesFeedSetting
        retval = BayesFeedSetting()
        #~ retval.user_id = self.id
        #~ retval.feed_id = feed_id
        #~ meta.Session.Add(retval)
        return retval

        #return h.find(lambda x:x.feed_id==2, c.user.bayes_feed_settings)
