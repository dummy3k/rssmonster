import logging

from datetime import datetime, timedelta, MINYEAR
from hashlib import md5
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
        retval = entry.title + " " + entry.summary
    else:
        retval = entry.title

    return h.strip_ml_tags(retval)

def add_spam_report(feed, spam_entries):
    if len(spam_entries) == 0:
        return
        
    c.entries = spam_entries
    c.baseurl = config['base_url']
    
    hasher = md5()
    #~ for entry in spam_entries:
        #~ hasher.update(entry.uid)
    
    ts = spam_entries[len(spam_entries)-1].updated
    title="RssMonster - Spam Summary - %s" % spam_entries[0].updated
    hasher.update(title)
    #log.debug("hasher.hexdigest() %s" % hasher.hexdigest())
    feed.add_item(title=title,
                  link="http://example.com",
                  description=render('bayes/spam_report.mako'),
                  unique_id=hasher.hexdigest(),
                  pubdate=ts)
                  

def cmp_updated(x,y):
    if not x.updated and not y.updated:
        return 0
    elif x.updated and not y.updated:
        return 1
    elif not x.updated and y.updated:
        return -1
    elif x.updated>y.updated:
        return 1
    elif x.updated==y.updated:
        return 0
    else: # x<y
        return -1
    

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

#        if untraind_id:            
#            guesser.trainer.untrain(other_pool, __relevant__(entry), untrain_id)
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
        spam_entries = []
        
        if request.params.get('report'):
            delta = h.timedelta_from_string(request.params.get('report'))
        else:
            delta = None
        
        log.debug("delta %s" % delta)

        settings = meta.Session\
                   .query(model.BayesFeedSetting)\
                   .filter_by(user_id = c.rss_user.id, feed_id=feed_data.id).first()
        if settings:
            meta.Session.update(settings)
            log.debug("settings.next_report (loaded): %s" % settings.next_report)
            entries = feed_data.get_entries().filter(model.FeedEntry.updated > settings.next_report).order_by(model.FeedEntry.updated)
        else:
            entries = feed_data.get_entries().order_by(model.FeedEntry.updated.desc()).limit(30)

            tmp = []
            for x in entries:
                tmp.append(x)
            entries = sorted(tmp, cmp_updated)
            
        for entry in entries:
            c.entry = entry
            c.entry.is_spam=guesser.is_spam(entry)

            if c.entry.is_spam and delta and entry.updated:
                log.debug("%s %s" % (entry.updated, entry.title[:40]))
                spam_entries.append(entry)

                if not settings:
                    settings = model.BayesFeedSetting()
                    settings.user_id = c.rss_user.id
                    settings.feed_id = feed_data.id
                    meta.Session.add(settings)
                    log.debug("settings.next_report (new): %s" % entry.updated)

                if not settings.next_report:
                    log.debug("first: %s" % entry.updated)
                    settings.next_report = entry.updated
                    
                elif settings.next_report + delta < entry.updated:
                    log.debug("next: %s" % entry.updated)
                    add_spam_report(feed, spam_entries)
                    
                    settings.next_report = entry.updated
                    spam_entries = []
            
                
            else:                
                if c.entry.is_spam:
                    titel = "[SPAM] %s" % entry.title
                else:
                    titel = entry.title

                feed.add_item(title=titel,
                              link=entry.link,
                              description=render('bayes/rss_summary.mako'),
                              unique_id=entry.uid,
                              pubdate=entry.updated) #entry.summary


        log.debug("len(spam_entries) = %s" % len(spam_entries))
        meta.Session.commit()
        
        if len(spam_entries) > 0:
            add_spam_report(feed, spam_entries)
    

        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
        
    def mixed_rss_with_report(self, user_id, id):
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
        spam_entries = []

        #~ settings = meta.Session\
                   #~ .query(model.BayesFeedSetting)\
                   #~ .filter_by(user_id = c.rss_user.id, feed_id=feed_data.id).first()
        settings = c.rss_user.get_bayes_feed_setting(feed_data.id)
        delta = h.timedelta_from_string(settings.summarize_at)
        log.debug("delta %s" % delta)

        #if not settings.next_report and not settings.last_report:
            #log.warn("no report dates (both), reading recent entries...")
            #entries = feed_data.get_entries().order_by(model.FeedEntry.updated.desc()).limit(30)

            #tmp = []
            #for x in entries:
                #tmp.append(x)
            #entries = sorted(tmp, cmp_updated)
            
            #settings.last_report = entries[0].updated - delta
            #settings.next_report = entries[0].updated + delta
            
        ##~ elif not settings.last_report:
            ##~ log.warn("no report dates (last), reading with other date")
            ##~ entries = feed_data.get_entries()\
                        ##~ .filter(model.FeedEntry.updated > settings.next_report-delta)\
                        ##~ .order_by(model.FeedEntry.updated)

        #else:
            #entries = feed_data.get_entries()\
                        #.filter(model.FeedEntry.updated > settings.last_report)\
                        #.order_by(model.FeedEntry.updated)
            

        entries = feed_data.get_entries()\
                    .order_by(model.FeedEntry.updated.desc())\
                    .limit(1000)
        
#            settings.next_report = datetime(MINYEAR, 1, 1)

        log.debug("settings.next_report: %s" % settings.next_report)
        log.debug("settings.last_report: %s" % settings.last_report)
        if not settings:
            h.flash("no intervall set")
            h.redirect_to(controller='feed', action='show_feed', id=feed_data.id)
            
        meta.Session.update(settings)


        reported = False
        cnt_surpressed = 0
        cnt_added = 0
        #max_entry_date = None
        for entry in entries:
            c.entry = entry
            c.entry.is_spam=guesser.is_spam(entry)

            if not c.entry.is_spam or not entry.updated:
                feed.add_item(title=entry.title,
                              link=entry.link,
                              description=render('bayes/rss_summary.mako'),
                              unique_id=entry.uid,
                              pubdate=entry.updated) #entry.summary

            elif entry.updated < settings.last_report:
                pass
            elif entry.updated < settings.last_report:
                #log.debug("add: %s %s" % (entry.updated, entry.title[:40]))
                cnt_added += 1
                spam_entries.append(entry)

            if entry.updated > settings.next_report:
                if not reported:
                    log.debug("report: %s" % len(spam_entries))
                    add_spam_report(feed, spam_entries)
                    reported = True

                    settings.last_report = entry.updated
                    settings.next_report = entry.updated + delta
                    spam_entries = []

                if c.entry.is_spam:
                    #log.debug("suppress: %s %s" % (entry.updated, entry.title[:40]))
                    cnt_surpressed += 1
#~ 
                #~ else:
                #~ #log.debug("suppress: %s %s" % (entry.updated, entry.title[:40]))
                    #~ cnt_surpressed += 1
                
                    #log.debug("next: %s" % entry.updated)
#                log.debug("report: %s %s" % (entry.updated, entry.title[:40]))
#                spam_entries.append(entry)
#        log.debug("len(spam_entries) = %s" % len(spam_entries))
        meta.Session.commit()
        
        #~ if len(spam_entries) > 0:
            #~ log.debug("report (last): %s" % len(spam_entries))
            #~ add_spam_report(feed, spam_entries)
            #~ reported = True
#~ 
            #~ settings.last_report = settings.next_report
            #~ settings.next_report = entry.updated + delta
    

        log.debug("cnt_added: %s" % cnt_added)
        log.debug("cnt_surpressed: %s" % cnt_surpressed)
        log.debug("last entry.updated: %s" % entry.updated)
        
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')

    def internal_rss_report(self):
        pass
        
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
        
    def change_intervall(self, id):
        word = request.params.get('word')
        settings = meta.Session\
                   .query(model.BayesFeedSetting)\
                   .filter_by(user_id = c.user.id, feed_id=id).first()
        if settings:
            meta.Session.update(settings)
        else:
            settings = model.BayesFeedSetting()
            settings.user_id = c.user.id
            settings.feed_id = id
            meta.Session.add(settings)

        settings.summarize_at = word
        meta.Session.commit()
        h.flash('changed intervall to %s' % word)
        return h.go_back()
        
