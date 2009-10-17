import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render
from rssmonster.model import meta
import rssmonster.model as model
import rssmonster.lib.helpers as h
#import rssmonster.lib.feedConverter

log = logging.getLogger(__name__)

def __find__(m, id):
    query = meta.Session.query(m)
    feed = query.filter(m.id == id).first()
    if not feed: 
        abort(404)

    return feed    

class FeedController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/feed.mako')
        # or, return a response
        return 'Hello World'
        
    def add(self):
        if not request.params.get('url'):
            return render('feed/add.mako')
            
        feed = model.Feed()
        feed.url = request.params.get('url')
        meta.Session.save(feed)
        meta.Session.commit()
        
        #return "url = %s" % request.params.get('url')
        return redirect_to(action='show_list')
        
    def show_list(self):
        query = meta.Session.query(model.Feed)
        c.feeds = query.all()
        c.links = [
            ('James','http://jimmyg.org'),
            ('Ben','http://groovie.org'),
            ('Philip',''),
        ]
        
        return render('feed/list.mako')
        
    def show_feed(self, id):
        c.feed = __find__(model.Feed, id)
        
        query = meta.Session.query(model.FeedEntry)
        c.entries = query.filter(model.FeedEntry.feed_id == id)
        
        return render('feed/show_feed.mako')

    def update(self, id):
        import feedparser

        feed = __find__(model.Feed, id)
        rss_reed = feedparser.parse(feed.url)
 #       return __dump__(rss_reed.feed)

        
        feed.title = rss_reed.feed.title
#        feed.last_builddate = rss_reed.feed.lastbuilddate
#        feed.updated = rss_reed.feed.updated_parsed
        feed.subtitle = rss_reed.feed.subtitle
        feed.language = rss_reed.feed.language
        feed.image = rss_reed.feed.image.href
        feed.link = rss_reed.feed.link
        meta.Session.update(feed)
       

        cnt_added = 0;
        for entry in rss_reed['entries']:
#            return __dump__(entry)
            feed_entry = model.FeedEntry()
            feed_entry.feed_id = id
            feed_entry.uid = entry['id']
            feed_entry.title = entry['title']
            feed_entry.summary = entry['summary']
            feed_entry.link = entry['link']
            meta.Session.save(feed_entry)
            cnt_added+=1

        meta.Session.commit()
#        return "added %s entries" % cnt_added
        h.flash("added %s entries" % cnt_added)
        return redirect_to(action='show_feed', Id=id)
        
        
