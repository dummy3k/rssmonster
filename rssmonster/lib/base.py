"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import session, tmpl_context as c

from rssmonster.model import meta

import logging
log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
            
        self.__do_stuff__()
        
    def __before__(self):                
        self.__do_stuff__()
        
    def __do_stuff__(self):
        try:
            c.user = session['user']
            log.debug("Hi FOOOOOOOOOO")
        except Exception as ex:
            log.debug(ex)
            pass
            
