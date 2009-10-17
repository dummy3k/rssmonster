import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from webhelpers.feedgenerator import Atom1Feed

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
        return render('feed/list.mako')
        
    def show_feed(self, id):
        c.feed = __find__(model.Feed, id)

#        query = meta.Session.query(model.FeedEntry)
#        c.entries = query.filter(model.FeedEntry.feed_id == id)
        c.entries = c.feed.get_entries()

        c.rss_feeds = [
            {'title':'Unmodified',
             'link':h.url_for(action='pipe')
            }
        ]
        
        
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
        if 'image' in rss_reed.feed:
            feed.image = rss_reed.feed.image.href
        feed.link = rss_reed.feed.link
        meta.Session.update(feed)
       

        cnt_added = 0;
        for entry in rss_reed['entries']:
            query = meta.Session.query(model.FeedEntry)
            feed_entry = query.filter_by(feed_id = id, uid = entry['id']).first()
            if not feed_entry:
                feed_entry = model.FeedEntry()
                is_new = True
            else:
                is_new = False
                
            feed_entry.feed_id = id
            feed_entry.uid = entry['id']
            feed_entry.title = entry['title']
            feed_entry.summary = entry['summary']
            feed_entry.link = entry['link']
            
            if is_new:
                meta.Session.save(feed_entry)
                cnt_added+=1
            else:
                meta.Session.update(feed_entry)
                

        meta.Session.commit()
        h.flash("added %s entries" % cnt_added)
        return redirect_to(action='show_feed', Id=id)
        
    def pipe(self, id):
        feed_data = __find__(model.Feed, id)
        feed = Atom1Feed(
            title=feed_data.title,
            link=feed_data.link,
            description=feed_data.subtitle,
            language=feed_data.language,
        )

        for entry in feed_data.get_entries():
            feed.add_item(title=entry.title,
                          link=entry.link,
                          description=entry.summary)

        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
                