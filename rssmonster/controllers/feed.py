import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from webhelpers.feedgenerator import Atom1Feed

from rssmonster.lib.base import BaseController, render
from rssmonster.model import meta
import rssmonster.model as model
import rssmonster.lib.helpers as h
#import rssmonster.lib.feedConverter
import bayes

log = logging.getLogger(__name__)

class FeedController(BaseController):

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
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())

        c.feed = meta.find(model.Feed, id)

#        query = meta.Session.query(model.FeedEntry)
#        c.entries = query.filter(model.FeedEntry.feed_id == id)
#        c.entries = c.feed.get_entries()
        guesser = bayes.Guesser(c.feed, c.user)
        c.entries = []
        query = c.feed.get_entries().order_by(model.FeedEntry.id.desc())
        for e in query: #.limit(10):
            e.is_spam=guesser.is_spam(e)
            e.score = guesser.guess(e)
            c.entries.append(e)

        from webhelpers import paginate
        c.page = paginate.Page(c.entries, request.params.get('page', 1))
        

#        from webhelpers import pagination
#        from webhelpers.pagination import links

#   http://bel-epa.com/pylonsdocs/thirdparty/webhelpers/paginate.html
#        total = len(c.entries)
#        c.paginator, c.entries_p = pagination.paginate(c.entries, per_page=10, item_count=total)
#        set_count = int(c.paginator.current)
#        total_pages = len(c.paginator)
#        c.pagelist = links.pagelist(c.paginator.current)

        c.rss_feeds = [
            {'title':'Unmodified',
             'link':h.url_for(action='pipe')
            },
            {'title':'Mixed',
             'link':h.url_for(controller='bayes', action='mixed_rss', user_id=c.user.id)
            }
        ]
        
        
        return render('feed/show_feed.mako')

    def update(self, id):
        feed = meta.find(model.Feed, id)
        cnt_added = self.__update__(feed)
        h.flash("added %s entries" % cnt_added)
        return h.go_back()
    
    def __update__(self, feed):
        import feedparser

        rss_reed = feedparser.parse(feed.url)
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
            feed_entry = query.filter_by(feed_id = feed.id, uid = entry['id']).first()
            if not feed_entry:
                feed_entry = model.FeedEntry()
                is_new = True
            else:
                is_new = False
                
            feed_entry.feed_id = feed.id
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
        
        
    def pipe(self, id):
        feed_data = meta.find(model.Feed, id)
        cnt_added = self.__update__(feed_data)

        feed = h.DefaultFeed(
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

