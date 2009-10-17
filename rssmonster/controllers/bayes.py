import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render
import rssmonster.lib.helpers as h

log = logging.getLogger(__name__)

def is_spam(entry):
    return (entry.id % 2 == 0)

class BayesController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/bayes.mako')
        # or, return a response
        return h.dump(response)
        
