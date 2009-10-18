import logging

from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render
import rssmonster.lib.helpers as h
from rssmonster.model import meta
import rssmonster.model as model

log = logging.getLogger(__name__)

def __relevant__(entry):
    if entry.summary:
        return entry.title + " " + entry.summary
    else:
        return entry.title

def myTokenizer():
    def tokenize(self, msg):
        retVal = []
        for token in msg.split():
            if len(token) < 10:
                continue
            
            token = token.lower()
            stopWords = ['is', 'the', 'for', 'of', 'to']
            if token in stopWords:
                continue

        return retVal

def my_tokenize(msg):
    retVal = []
    for token in msg.split():
        if len(token) < 4:
            continue
        
        token = token.lower()
        stopWords = ['is', 'the', 'for', 'of', 'to']
        if token in stopWords:
            continue

        retVal.append(token)
        
    return retVal

from reverend.thomas import Bayes
    
class Guesser():
    
    def __init__(self, feed, user):
        import os.path
        
        self.user = user
        self.filename = config['bayes_dir']
        self.filename += "/users/%s" % user.id
        if not os.path.exists(self.filename):
            os.makedirs(self.filename)
        self.filename += '/feed_%s.bayes' % str(feed.id)
        log.debug("filename:%s" % self.filename)

        self.trainer = Bayes(tokenizer=myTokenizer())
        self.trainer.getTokens = my_tokenize
        if os.path.exists(self.filename):
            self.trainer.load(self.filename)
        else:
            self.trainer.newPool('ham')
            self.trainer.newPool('spam')

    def save(self):
        self.trainer.save(self.filename)

    def clear(self):
        self.trainer = Bayes(tokenizer=myTokenizer())
        self.trainer.getTokens = my_tokenize
        self.trainer.newPool('ham')
        self.trainer.newPool('spam')
    
    def is_spam(self, entry):
        classy = meta.Session\
                .query(model.Classification)\
                .filter_by(user_id = self.user.id, entry_id=entry.id).first()
        if classy:
            if classy.pool == 'spam':
                return True
            elif classy.pool == 'ham':
                return False
            else:
                raise "bad pool"
                                
        g = self.guess(entry)

        if g['spam'] and not g['ham']:
            return True
            
        if not g['spam'] and g['ham']:
            return False
            
        return (g['spam'] > g['ham'])

    def guess(self, entry):
        log.debug("__relevant__(entry) %s" % __relevant__(entry))
        log.debug("__relevant__(entry) %s" % self.trainer.guess(__relevant__(entry)))
        log.debug('self.filename: %s' % self.filename)
#        ret = dict(self.trainer.guess(__relevant__(entry)))
        ret = dict(self.trainer.guess(__relevant__(entry)))
        log.debug("ret: %s" % ret)
        if not 'spam' in ret:
            ret['spam'] = None
        if not 'ham' in ret:
            ret['ham'] = None
        
        return ret
            

class BayesController(BaseController):

    def mark_as_spam(self, id):
        return self.__mark_as__(id, 'spam')
        
    def mark_as_ham(self, id):
        return self.__mark_as__(id, 'ham')

    def __mark_as__(self, id, pool):
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())
            
        entry = meta.find(model.FeedEntry, id) 
        feed = meta.find(model.Feed, entry.feed_id)

        classy = meta.Session\
                .query(model.Classification)\
                .filter_by(user_id = c.user.id, entry_id=entry.id).first()

        if not classy:
            classy = model.Classification()
            classy.user_id = c.user.id
            classy.entry_id = id
            classy.pool = pool
            meta.Session.save(classy)
            
            untrain_id = None
        else:
            if classy.pool == pool:
                h.flash("entry was already classified")
                #return redirect_to(controller='feed', action='show_feed', id=entry.feed_id)
            
            classy.pool = pool
            meta.Session.update(classy)

            untrain_id = entry.id
            
        meta.Session.commit()

        guesser = Guesser(feed, c.user)
        guesser.trainer.train(pool, __relevant__(entry)) #, entry.id
        
        if pool == 'spam':
            other_pool = 'ham'
        elif pool == 'ham':
            other_pool = 'spam'
        else:
            raise "bad pool"
            
        guesser.trainer.untrain(other_pool, __relevant__(entry)) #, untrain_id
        guesser.save()

        h.flash("now known as %s: %s" % (pool, entry.id))
        return redirect_to(controller='feed', action='show_feed', id=entry.feed_id)

    def show_score(self, id):
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())

        c.entry = meta.find(model.FeedEntry, id) 
        
        feed = meta.find(model.Feed, c.entry.feed_id)
        c.feed = feed
        guesser = Guesser(feed, c.user)
        guess = guesser.guess(c.entry)

        log.debug("guess: %s" % guess)
        log.debug("c.entry.title: %s" % c.entry.title)
        
        c.score = str(guess)
        c.score = guesser.guess(c.entry)
        c.pool = guesser.trainer.poolData('spam')
        c.is_spam = guesser.is_spam(c.entry)

        import operator
        c.pool_data_spam = guesser.trainer.poolData('spam')
        c.pool_data_spam.sort(key=operator.itemgetter(1))
        c.pool_data_spam.reverse()

        c.pool_data_ham = guesser.trainer.poolData('ham')
        c.pool_data_ham.sort(key=operator.itemgetter(1))
        c.pool_data_ham.reverse()
        
        c.tokens = set(guesser.trainer.getTokens(__relevant__(c.entry)))
        
        c.actions = [{'link':h.url_for(controller='feed', action='show_feed', id=feed.id),
                        'text':'Feed Details'}]
        return render('bayes/score.mako')
        
    def show_guesser(self, id):
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())

        c.feed = meta.find(model.Feed, id)
        guesser = Guesser(c.feed, c.user)

        import operator
        c.pool_data_spam = guesser.trainer.poolData('spam')
        c.pool_data_spam.sort(key=operator.itemgetter(1))
        c.pool_data_spam.reverse()

        c.pool_data_ham = guesser.trainer.poolData('ham')
        c.pool_data_ham.sort(key=operator.itemgetter(1))
        c.pool_data_ham.reverse()
        
        c.actions = [{'link':h.url_for(controller='feed', action='show_feed', id=id),
                        'text':'Feed Details'}]
        return render('bayes/guesser.mako')
    
    def mixed_rss(self, user_id, id):
        user = meta.find(model.User, user_id)
        feed_data = meta.find(model.Feed, id)
        
        import feed
        cnt_added = feed.__update__(feed_data)

        feed = h.DefaultFeed(
            title=feed_data.title,
            link=feed_data.link,
            description="TESTING",
            language=feed_data.language,
        )

        c.base_url = config['base_url']
        log.debug('c.base_url: %s' % c.base_url)

        guesser = Guesser(feed_data, user)
        for entry in feed_data.get_entries():
            c.entry = entry
            c.entry.is_spam=guesser.is_spam(entry)
            if c.entry.is_spam:
                titel = "[SPAM] %s" % entry.title
            else:
                titel = entry.title

            feed.add_item(title=titel,
                          link=entry.link,
                          description=render('bayes/rss_summary.mako')) #entry.summary

        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
        
    def redo(self, id):
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())

        c.feed = meta.find(model.Feed, id)

        query = meta.Session\
                .query(model.Classification)\
                .join(model.FeedEntry)\
                .filter_by(feed_id=id)

        guesser = Guesser(c.feed, c.user)
        guesser.clear()

        cnt = 0
        for entry in query:
            h.flash("%s :%s" % (entry.pool, __relevant__(entry.entry)))
            guesser.trainer.train('spam', __relevant__(entry.entry))
            cnt+=1

        guesser.save()
        h.flash("learned %s entries" % cnt)
        return h.go_back()
    
