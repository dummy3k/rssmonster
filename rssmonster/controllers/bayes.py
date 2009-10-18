import logging

from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render
import rssmonster.lib.helpers as h
from rssmonster.model import meta
import rssmonster.model as model

log = logging.getLogger(__name__)

class Guesser():
    def __init__(self, feed):
        import os.path
        from reverend.thomas import Bayes
        
        self.filename = config['bayes_dir']
        if not os.path.exists(self.filename):
            os.makedirs(self.filename)
        self.filename += '/feed_%s.bayes' % feed.id
        log.debug("filename:%s" % self.filename)

        self.trainer = Bayes()
        if os.path.exists(self.filename):
            self.trainer.load(self.filename)
        else:
            self.trainer.newPool('ham')
            self.trainer.newPool('spam')

    def save(self):
        self.trainer.save(self.filename)

    def is_spam(self, entry):
        g = self.guess(entry)

        if g['spam'] and not g['ham']:
            return True
            
        if not g['spam'] and g['ham']:
            return False
            
        return (g['spam'] > g['ham'])

    def guess(self, entry):
        ret = dict(self.trainer.guess(entry.title))
        if not 'spam' in ret:
            ret['spam'] = None
        if not 'ham' in ret:
            ret['ham'] = None
        
        return ret
            

class BayesController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/bayes.mako')
        # or, return a response
        return h.dump(response)

    def mark_as_spam(self, id):
        entry = meta.find(model.FeedEntry, id) 
        feed = meta.find(model.Feed, entry.feed_id)

        guesser = Guesser(feed)
        guesser.trainer.train('spam', entry.title, entry.id)
        guesser.trainer.untrain('ham', entry.title, entry.id)
        guesser.save()
        
        h.flash("i understand that you don't like: %s" % entry.title)
        return redirect_to(controller='feed', action='show_feed', id=entry.feed_id)
        
    def mark_as_ham(self, id):
        entry = meta.find(model.FeedEntry, id) 
        feed = meta.find(model.Feed, entry.feed_id)

        guesser = Guesser(feed)
        guesser.trainer.train('ham', entry.title, entry.id)
        guesser.trainer.untrain('spam', entry.title, entry.id)
        guesser.save()
        
        h.flash("you really seem to like: %s" % entry.title)
        return redirect_to(controller='feed', action='show_feed', id=entry.feed_id)
        
    def show_score(self, id):
        c.entry = meta.find(model.FeedEntry, id) 
        
        feed = meta.find(model.Feed, c.entry.feed_id)
        guesser = Guesser(feed)
        guess = guesser.trainer.guess(c.entry.title)
        log.debug("guess: %s" % guess)
        
        c.score = str(guess)
        return render('bayes/score.mako')
        
    def show_guesser(self, id):
        import operator
        
        c.feed = meta.find(model.Feed, id)

        guesser = Guesser(c.feed)
        c.pool_data_spam = guesser.trainer.poolData('spam')
        c.pool_data_spam.sort(key=operator.itemgetter(1))
        c.pool_data_spam.reverse()

        c.pool_data_ham = guesser.trainer.poolData('ham')
        c.pool_data_ham.sort(key=operator.itemgetter(1))
        c.pool_data_ham.reverse()
        
        c.actions = [{'link':h.url_for(controller='feed', action='show_feed', id=id),
                        'text':'Feed Details'}]
        return render('bayes/guesser.mako')
    
    def untrain(self, id):
        c.entry = meta.find(model.FeedEntry, id) 
        c.feed = meta.find(model.Feed, c.entry.feed_id)
        guesser = Guesser(c.feed)

        guesser.trainer.untrain('spam', c.entry.title, c.entry.id)
        guesser.save()
        h.flash("untrained: %s" % c.entry.title)

        return redirect_to(action='show_guesser', id=c.entry.feed_id)
            
        
