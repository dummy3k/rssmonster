import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render

log = logging.getLogger(__name__)

class FeedController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/feed.mako')
        # or, return a response
        return 'Hello World'
        
    def add(self):
        return "url = %s" % request.params.get('url')
