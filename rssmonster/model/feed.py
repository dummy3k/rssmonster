from sqlalchemy import *
import meta
import hashlib
from datetime import datetime
from feed_entries import FeedEntry

import logging
log = logging.getLogger(__name__)

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

    def get_entries(self):
        query = meta.Session.query(FeedEntry)
        return query.filter(FeedEntry.feed_id == self.id)

    def fetch(self):
        import feedparser

        rss_reed = feedparser.parse(self.url)
        if not rss_reed:
            raise "failed to fetch feed"

        if hasattr(rss_reed.feed,'title'):
	        self.title = rss_reed.feed.title
        else:
            log.warn("feed %s has no title" % self.id)
    #        self.last_builddate = rss_reed.feed.lastbuilddate
    #        self.updated = rss_reed.feed.updated_parsed
        self.subtitle = rss_reed.feed.subtitle
        if 'language' in rss_reed.feed:
            self.language = rss_reed.feed.language
        if 'image' in rss_reed.feed:
            self.image = rss_reed.feed.image.href
        self.link = rss_reed.feed.link
        meta.Session.update(self)

        
        cnt_added = 0;
        for entry in rss_reed['entries']:
#            query = meta.Session.query(model.FeedEntry)
#            feed_entry = query.filter_by(feed_id = self.id, uid = entry['id']).first()
#            log.debug("self.entries: %s" % self.entries)
#            log.debug("self.entries: %s" % dir(self.entries))
            if self.entries:
                feed_entry = filter((lambda y: y.uid==entry['id']), self.entries)
                if feed_entry:
                    feed_entry = feed_entry[0]
            else:
                feed_entry = None

            if not feed_entry:
                log.debug("fetched new entry '%s' from '%s'" % (entry['title'][:20], rss_reed.feed.title[:20]))
                feed_entry = FeedEntry()
                is_new = True
            else:
                is_new = False
                
            log.debug("entry: %s" % entry)
            feed_entry.feed_id = self.id
            feed_entry.uid = entry['id']
            feed_entry.title = entry['title']
            if 'summary' in entry:
                feed_entry.summary = entry['summary']
            feed_entry.link = entry['link']
            
            if is_new:
                meta.Session.save(feed_entry)
                cnt_added+=1
            else:
                meta.Session.update(feed_entry)
                

        meta.Session.commit()
        return cnt_added
        


