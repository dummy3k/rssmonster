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

        rss_feed = feedparser.parse(self.url)
        if not rss_feed:
            raise "failed to fetch feed"

        if not 'entries' in rss_feed:
	        log.error("no entries while fetching '%s'" % self.title)
	        from pylons.controllers.util import abort
	        abort(503)
	        
        if 'title' in rss_feed.feed:
	        self.title = rss_feed.feed.title
        else:
            log.warn("feed %s has no title" % self.id)
            
#        if hasattr(rss_feed.feed,'subtitle'):
        if 'subtitle' in rss_feed.feed:
	        self.subtitle = rss_feed.feed.subtitle
        else:
            log.warn("feed %s has no subtitle" % self.id)
            
            
    #        self.last_builddate = rss_feed.feed.lastbuilddate
    #        self.updated = rss_feed.feed.updated_parsed
        if 'language' in rss_feed.feed:
            self.language = rss_feed.feed.language
        if 'image' in rss_feed.feed:
            self.image = rss_feed.feed.image.href
            
        if 'link' in rss_feed.feed:
	        self.link = rss_feed.feed.link
        else:
            log.warn("feed %s has no link" % self.id)

        self.last_fetch = datetime.now()
        meta.Session.update(self)

        retval = {'cnt_added':0, 'is_up2date':False}
#        retval.is_up2date = False
#        retval.cnt_added = 0;
        for entry in rss_feed['entries']:
#            query = meta.Session.query(model.FeedEntry)
#            feed_entry = query.filter_by(feed_id = self.id, uid = entry['id']).first()
#            log.debug("self.entries: %s" % self.entries)
#            log.debug("self.entries: %s" % dir(self.entries))
            if self.entries:
                feed_entry = filter((lambda y: y.uid==entry['id']), self.entries)
                if feed_entry:
                    feed_entry = feed_entry[0]
                    retval['is_up2date'] = True
            else:
                feed_entry = None

            if not feed_entry:
                log.debug("fetched new entry '%s' from '%s'" % (entry['title'][:20], rss_feed.feed.title[:20]))
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
                retval['cnt_added']+=1
            else:
                meta.Session.update(feed_entry)
                

        meta.Session.commit()
        
        if not retval['is_up2date']:
            log.warn("feed '%s' is not up to date" % self.title)
        return retval
        


