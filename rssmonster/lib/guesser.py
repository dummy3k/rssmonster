import logging
from pylons import config
from reverend.thomas import Bayes
from rssmonster.model import meta
import helpers as h
import rssmonster.model as model

log = logging.getLogger(__name__)

def my_tokenize(msg):
    retVal = []
    log.debug("msg: %s" % msg)
    msg = h.markdown(msg, safe_mode="remove")
    log.debug("!!!!!msg: %s" % msg)
    for token in msg.split():
        log.debug("token: %s" % token)
        if len(token) < 4:
            continue
        
        token = token.lower()
        stopWords = ['is', 'the', 'for', 'of', 'to']
        if token in stopWords:
            continue

        retVal.append(token)
        
    return retVal

            
    
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

        self.trainer = Bayes()
        self.trainer.getTokens = my_tokenize
        if os.path.exists(self.filename):
            self.trainer.load(self.filename)
        else:
            self.trainer.newPool('ham')
            self.trainer.newPool('spam')

    def save(self):
        self.trainer.save(self.filename)

    def clear(self):
        self.trainer = Bayes()
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
        from rssmonster.controllers.bayes import __relevant__
        
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
