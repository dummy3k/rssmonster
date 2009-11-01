import logging

from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render
import rssmonster.lib.helpers as h
from rssmonster.lib.guesser import Guesser
from rssmonster.model import meta
import rssmonster.model as model
from pylons.controllers.util import redirect

log = logging.getLogger(__name__)

def __relevant__(entry):
    if entry.summary:
        return entry.title + " " + entry.summary
    else:
        return entry.title

class BayesController(BaseController):

    def mark_as_spam(self, id):
        log.debug("FFF!")

        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())
            
        entry = meta.find(model.FeedEntry, id) 
        feed = meta.find(model.Feed, entry.feed_id)
        guesser = Guesser(feed, c.user)
        return self.__mark_as__(entry, 'spam', guesser)
        
    def mark_as_ham(self, id):
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())
            
        entry = meta.find(model.FeedEntry, id) 
        feed = meta.find(model.Feed, entry.feed_id)
        guesser = Guesser(feed, c.user)
        return self.__mark_as__(entry, 'ham', guesser)

    def __mark_as__(self, entry, pool, guesser, force=False):
        """ when forced the entry is updated even if the db says it is already """
        log.debug("entry.id: %s" % entry.id)
        classy = meta.Session\
                .query(model.Classification)\
                .filter_by(user_id = c.user.id, entry_id=entry.id).first()

        if not classy:
            classy = model.Classification()
            classy.user_id = c.user.id
            classy.entry_id = entry.id
            classy.pool = pool
            meta.Session.save(classy)
            
            untrain_id = None
        else:
            if classy.pool == pool and not force:
                h.flash("entry was already classified as %s" % pool)
                return h.go_back(h.url_for(controller='feed', action='show_feed', id=entry.feed_id))
                #return redirect_to(controller='feed', action='show_feed', id=entry.feed_id)
            
            classy.pool = pool
            meta.Session.update(classy)

            untrain_id = entry.id
            
        meta.Session.commit()

        guesser.trainer.train(pool, __relevant__(entry), entry.id)
        
        if pool == 'spam':
            other_pool = 'ham'
        elif pool == 'ham':
            other_pool = 'spam'
        else:
            raise "bad pool"
            
#        guesser.trainer.untrain(other_pool, __relevant__(entry), untrain_id)
        guesser.save()

        if not force:
            h.flash("now known as %s: %s" % (pool, entry.id))
            return h.go_back(h.url_for(controller='feed', action='show_feed', id=entry.feed_id))

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
#        c.pool_data_spam = map(lambda x: (x[0], x[1], x[0].encode('ascii', 'ignore')), c.pool_data_spam)

        c.pool_data_ham = guesser.trainer.poolData('ham')
        c.pool_data_ham.sort(key=operator.itemgetter(1))
        c.pool_data_ham.reverse()
        
        c.actions = [{'link':h.url_for(controller='feed', action='show_feed', id=id),
                        'text':'Feed Details'}]
                        
        c.stopwords = meta.Session\
            .query(model.Stopword)\
            .filter_by(feed_id=id, user_id=c.user.id)

        return render('bayes/guesser.mako')
    
    def mixed_rss(self, user_id, id):
        c.rss_user = meta.find(model.User, user_id)
        log.debug("c.rss_user: %s" % c.rss_user)
        feed_data = meta.find(model.Feed, id)
        log.debug("feed_data.id %s" % feed_data.id)
        
        import feed
        fetch_result = feed_data.fetch()

        feed = h.DefaultFeed(
            title=feed_data.title,
            link=feed_data.link,
            description="TESTING",
            language=feed_data.language,
        )

        c.base_url = config['base_url']
        log.debug('c.base_url: %s' % c.base_url)

        guesser = Guesser(feed_data, c.rss_user)
        last_summary = None
        for entry in feed_data.get_entries().order_by(model.FeedEntry.id.desc()).limit(30):
            log.debug(entry)
            c.entry = entry
            c.entry.is_spam=guesser.is_spam(entry)
            if c.entry.is_spam:
                titel = "[SPAM] %s" % entry.title
            else:
                titel = entry.title

            feed.add_item(title=titel,
                          link=entry.link,
                          description=render('bayes/rss_summary.mako'),
                          unique_id=entry.uid) #entry.summary

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
        needles_cnt = 0
        for entry in query:
#            h.flash("%s :%s" % (entry.pool, __relevant__(entry.entry)))
#            guesser.trainer.train(entry.pool, __relevant__(entry.entry))

            if guesser.is_spam(entry.entry, use_classified=False) and (entry.pool == 'spam'):
                needles_cnt += 1
            elif not guesser.is_spam(entry.entry, use_classified=False) and (entry.pool == 'ham'):
                needles_cnt += 1

            self.__mark_as__(entry.entry, entry.pool, guesser, True)
            cnt+=1

        guesser.save()
        log.debug("FOOOOOO")
        
        
        if needles_cnt > 0:
            h.flash("%d entries were needlessly trained (total: %s)" % (needles_cnt, cnt))
        else:
            h.flash("learned %s entries" % cnt)
        
        return h.go_back()
        
    def mark_stopword(self, id, word):
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())

        w = model.Stopword()
        w.user_id = c.user.id
        w.feed_id = id
        w.word = word
        meta.Session.save(w)
        
        from sqlalchemy.exceptions import IntegrityError
        try:
            meta.Session.commit()
            h.flash("%s? Never heard about it." % word)
        except IntegrityError:
            h.flash("i already know that '%s' is a stop word." % word)
            meta.Session.rollback()
        
        return self.redo(id)
        
    def unmark_stopword(self, id, word):
        if not c.user:
            return redirect_to(controller='login', action='signin', id=None, return_to=h.url_for())

        w = meta.Session.query(model.Stopword).filter_by(user_id=c.user.id, feed_id=id, word=word).first()
        if not w:
            h.flash("can't remove '%s', because it is not on the list." % word)

        log.debug("w: %s" % w)            
        meta.Session.delete(w)
        
        from sqlalchemy.exceptions import IntegrityError
        meta.Session.commit()
        h.flash("removed '%s' from stopwords list." % word)
        
        return self.redo(id)
        
    
