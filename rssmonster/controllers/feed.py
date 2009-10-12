import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render
from rssmonster.model import meta
import rssmonster.model as model
import rssmonster.lib.helpers as h

log = logging.getLogger(__name__)

class FeedController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/feed.mako')
        # or, return a response
        return 'Hello World'
        
    def add(self):
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
        
