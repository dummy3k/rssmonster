from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from rssmonster.lib.base import BaseController, render
from rssmonster.model import meta
import rssmonster.model as model
import rssmonster.lib.helpers as h

from openid.consumer.consumer import Consumer, SUCCESS, FAILURE, DiscoveryFailure
from openid.store.sqlstore import SQLiteStore, MySQLStore 
#from openid import sreg
from openid.extensions import sreg
from datetime import datetime
from pylons.i18n import get_lang, set_lang
from pylons.decorators import rest
from rssmonster.lib.base import *
from gettext import gettext as _
from datetime import datetime

from webhelpers.pylonslib import Flash as _Flash
flash = _Flash()

log = logging.getLogger(__name__)

class LoginController(BaseController):
    def __before__(self):                
        BaseController.__before__(self)
        
        self.openid_session = session.get("openid_session", {})
        log.debug("__before__.openid_session %s" % self.openid_session)
        
        con = meta.engine.raw_connection()
        if config['sqlalchemy.url'].find('mysql:') != -1:
            self.store = MySQLStore(con);
        else:
            self.store = SQLiteStore(con);
                
    @rest.dispatch_on(POST="update_account")
    def index(self):
        if not c.user:
            redirect_to(action='signin')
            
        h.flash(_("Already signed in."))
        return h.go_back()
        

#    @validate(template='account.index', schema=schema.UpdateUser(), form='index',
#              variable_decode=True)

    def update_account(self):
        log.debug('update_account()')
        
        if 'language' in request.POST:
            redirect_to(action='index', id=None)
        print request.POST
        query = meta.Session.query(model.User)
        user = query.filter_by(openid=request.POST['openid']).first()
        user.name = request.POST['name']
        if 'email' in request.POST:
            user.email = request.POST['email']
        user.tzinfo = request.POST['tzinfo']
        #user.language = request.POST['language']
        meta.Session.commit()
        redirect_to(action='index')

    @rest.dispatch_on(POST="signin_POST")
    def signin(self):
        log.debug("enter signin()")
        if c.user:
            h.flash(_("Already signed in."))
            return h.go_back()

        c.return_to = request.params.get('return_to', None)
        return render('login/signin.mako')

    def signin_POST(self):
        log.debug("enter signin_POST()")
        problem_msg = _('A problem ocurred comunicating to your OpenID server. Please try again.')

        self.consumer = Consumer(self.openid_session, self.store)
        openid = request.params.get('openid', None)
        if openid is None:
            log.warn("openid is None")
            h.flash(problem_msg)
            return render('login/signin.mako')
        try:
            authrequest = self.consumer.begin(openid)
        except DiscoveryFailure, e:
            log.warn(e)
            log.warn("OpenID URL: " + openid)
            h.flash(problem_msg)
            return redirect_to(action='signin')
        
        sreg_request = sreg.SRegRequest(
            #required=['email'],
            optional=['fullname', 'timezone', 'language', 'email']
        )

        authrequest.addExtension(sreg_request)
        redirecturl = authrequest.redirectURL(config['base_url'],
            #h.url_for(controller='main', action='index', qualified=True),
            return_to=config['base_url'] + h.url_for(action='verified', qualified=False, 
                                                     return_to=request.params.get('return_to', None)),
            immediate=False
        )
        log.debug("redirecturl: %s" % redirecturl)
        session['openid_session'] = self.openid_session
        session.save()
        return redirect_to(redirecturl)
    
    def success(self):
        return "foo"
        return h.go_back()

    def verified(self):
        log.debug("enter verified()")
        log.debug("openid_session = %s" % self.openid_session)
        problem_msg = _('A problem ocurred comunicating to your OpenID server. Please try again.')
        self.consumer = Consumer(self.openid_session, self.store)
        info = self.consumer.complete(request.params,
                                      (h.url_for(action='verified',
                                                 qualified=True)))
        if info.status == SUCCESS:
            query = meta.Session.query(model.User)
            user = query.filter_by(openid=info.identity_url).first()
            
            newUser = user is None
            
            if user is None:
                user = model.User()
                user.openid=info.identity_url
                user.signup = datetime.now()
                user.reputation = 0
                #meta.Session.add(user)
                #meta.Session.commit()
                log.debug("first contact with user '%s'" % info.identity_url)
                
            if user.banned:
                redirect_to(action='banned')
                
            user.updatelastlogin()
            if newUser:
                sreg_response = sreg.SRegResponse.fromSuccessResponse(info)
                if sreg_response:
                    user.name = sreg_response.get('fullname', u'')
                    user.email = sreg_response.get('email', u'')
        #            user.tzinfo = sreg_response.get('timezone', u'')
        #            user.tzinfo = sreg_response.get('language', u'')
        
                meta.Session.save(user)
            else:
                meta.Session.update(user)
            meta.Session.commit()
            #session.clear()
            session['openid'] = info.identity_url
            
            h.flash(_("Signed in"))
            
            session['user'] = user
            session.save()
            log.debug('on verified before session check')
            log.debug('user = %s' % dir(user))

            return h.go_back()
            
        else:
            log.warn("verified, but no success")
            log.debug("info: %s" % info)
            
            h.flash(problem_msg)
            return redirect_to(action='signin')

    def signout(self):
        if not c.user:
            h.flash(_("You are not signed in."))
            h.go_back()
            
        session.clear()
        h.flash(_("You've been signed out."))

        h.go_back()

    def banned(self):
        if not c.user:
            h.flash(_("You are not signed in."))
            return redirect_to(action='signin')
        if not c.user.banned:
            h.flash(_("You are not banned."))
            return h.go_back()

        return render('login/account-banned.mako')

    def signedin(self):
        return session['signedin']
        
    def offline_login(self):
        identity_url = "http://www.example.com"
        username = "offline"
        
        query = meta.Session.query(model.User)
        user = query.filter_by(name=username).first()
        
        newUser = user is None
        
        if newUser:
            user = model.User()
            user.name=username
            user.openid=identity_url
            user.signup = datetime.now()
            user.reputation = 0

        user.updatelastlogin()
        
        if newUser:
            meta.Session.add(user)
        else:
            meta.Session.update(user)
            
        meta.Session.commit()
        #session.clear()
        session['openid'] = identity_url
        
        h.flash(_("Signed in"))
        
        session['user'] = user
        session.save()

        if 'returnTo' in session:
            controller = session['returnTo'].get('controller', None)
            action = session['returnTo'].get('action', None)
            id = session['returnTo'].get('id', None)
            istrue = istrue=session['returnTo'].get('istrue', None)

            del session['returnTo']
            session.save()

            return redirect_to(controller=controller, action=action, id=id, istrue=istrue)
        else:
            return h.go_back()

