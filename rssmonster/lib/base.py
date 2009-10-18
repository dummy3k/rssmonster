"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import session, tmpl_context as c

from rssmonster.model import meta, user

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
        if 'openid' in session:
            c.user = meta.Session.query(user.User).filter_by(openid = session['openid']).first()
        else:
            c.user = None
        return

        c.user = None
        log.debug("session: %s" % session)
        log.debug("c.user.id: %s" % session['openid'])
        log.debug("dir(session): %s" % dir(session))

        if 'user' in session and session['user']:
            c.user = session['user']
            log.debug("Yeah!")
            log.debug("c.user.id: %s" % session['user'])
        else:
            c.user = 'not logged in'

        log.debug("c.user.id: %s" % 'c.user')

#        try:
#            c.user = session['user']
#        except Exception as ex:
#            log.debug("exception: %s" % ex)
#            pass
            
