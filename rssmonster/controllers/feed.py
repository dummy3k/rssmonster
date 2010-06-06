import logging

from pylons import request, response, session, tmpl_context as c
from pylons import url, config
from pylons.controllers.util import abort, redirect
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
        return redirect(url(controller='feed', action='show_list'))
        
    def show_list(self):
        query = meta.Session.query(model.Feed)
        c.feeds = query.all()
        return render('feed/list.mako')
        
    def show_feed(self, id, page=1):
        if not c.user:
            return redirect(url(controller='login', action='signin', id=None, return_to=url.current()))

        c.feed = meta.find(model.Feed, id)
        guesser = bayes.Guesser(c.feed, c.user, config)
        query = c.feed.get_entries().order_by(model.FeedEntry.updated.desc()) #.limit(30)

        from webhelpers import paginate
        c.page = paginate.Page(query, page)

        for e in c.page.items:
            e.is_spam=guesser.is_spam(e)
            e.score = guesser.guess(e)

        c.last_spam_entries = []
        c.last_ham_entries = []
        i = 0
        for e in query.limit(500):
            e.is_spam=guesser.is_spam(e)

            if len(c.last_spam_entries) < 10 and e.is_spam:
                c.last_spam_entries.append(e)

            if len(c.last_ham_entries) < 10 and not e.is_spam:
                c.last_ham_entries.append(e)
                
            if len(c.last_spam_entries) >= 10 and len(c.last_ham_entries) >= 10:
                log.debug("breaking loop after %s rows" % i)
                break

            i += 1
        

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
             'link':h.url_for(controller='feed', action='pipe')
            },
            {'title':'Mixed',
             'link':h.url_for(controller='bayes', action='mixed_rss', user_id=c.user.id)
            },
            {'title':'Mixed with Report',
             'link':h.url_for(controller='bayes', action='mixed_rss_with_report', user_id=c.user.id)
            }
        ]
        
        
        
        
#        import operator
#        ret = self.entries
#        ret.sort(lambda x,y: -cmp(x.id, y.id))
#        return ret[:10]        
        
        
        return render('feed/show_feed.mako')

    def update(self, id):
        feed = meta.find(model.Feed, id)
        cnt_added = feed.fetch()
        h.flash("added %s entries" % cnt_added)
        return h.go_back()

    def pipe(self, id):
        feed_data = meta.find(model.Feed, id)
        cnt_added = feed_data.fetch()

        feed = h.DefaultFeed(
            title=feed_data.title,
            link=feed_data.link,
            description=feed_data.subtitle,
            language=feed_data.language,
        )

        for entry in feed_data.get_entries():
            feed.add_item(title=entry.title,
                          link=entry.link,
                          description=entry.summary,
                          unique_id=entry.uid)

        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')

    def show_record(self, id):
        c.feed = meta.find(model.Feed, id)
        return render('feed/record.mako')
        
