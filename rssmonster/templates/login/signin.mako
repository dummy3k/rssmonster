<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Sign in</%def>

<%def name="content()">
    <h1>${_('Sign in with OpenID')}</h1>

    <form id="signin-form" method="post" action="${h.url_for(controller='login', action='signin_POST')}">
        <input type='hidden' name='return_to' value='${c.return_to}' />
        <table border="0">
            <tr>
                <td>
                    <input type="text" name="openid" id="openid" class="openid-identifier" />
                </td>
                <td>
                    <input type="submit" value="Login" class="openid-login-button" />
                </td>
            </tr>
        </table>
    </form>
    
    <br/><br/>
    <p>
        ${_('Dont forget to enable OpenID support with your preferred provider first!')}
    </p>

    <div class="openid-links">
        <a class="openid_large_btn" style="background: rgb(255, 255, 255) url(../img/openid/openid.png) no-repeat center center;" href="javascript: signin('openid');" title="OpenID"></a>
        <a class="openid_large_btn" style="background: rgb(255, 255, 255) url(../img/openid/google.png) no-repeat center center;" href="javascript: signin('google');" title="Google"></a>
        <a class="openid_large_btn" style="background: rgb(255, 255, 255) url(../img/openid/yahoo.png) no-repeat center center;" href="javascript: signin('yahoo');" title="Yahoo"></a>
        <a class="openid_large_btn" style="background: rgb(255, 255, 255) url(../img/openid/aol.png) no-repeat center center;" href="javascript: signin('aol');" title="AOL"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/myopenid.png) no-repeat center center;" href="javascript: signin('myopenid');" title="MyOpenID"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/livejournal.png) no-repeat center center;" href="javascript: signin('livejournal');" title="LiveJournal"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/flickr.png) no-repeat center center;" href="javascript: signin('flickr');" title="Flickr"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/technorati.png) no-repeat center center;" href="javascript: signin('technorati');" title="Technorati"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/wordpress.png) no-repeat center center;" href="javascript: signin('wordpress');" title="Wordpress"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/blogger.png) no-repeat center center;" href="javascript: signin('blogger');" title="Blogger"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/verisign.png) no-repeat center center;" href="javascript: signin('verisign');" title="Verisign"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/vidoop.png) no-repeat center center;" href="javascript: signin('vidoop');" title="Vidoop"></a>
        <a class="openid_small_btn" style="background: rgb(255, 255, 255) url(../img/openid/claimid.png) no-repeat center center;" href="javascript: signin('claimid');" title="ClaimID"></a>
    </div>
    
    <div id="openid-prompt">
        <div id="openid-provider-prompt">${_('Your Account:')}</div>
        <div id="openid-provider-username"><input id="openid-username" name="openid-username" value="" /></div>
        <div id="openid-provider-login"><input id="openid-login" type="submit" value="Login" /></div>
        <input type="hidden" id="openid-provider-url" value="" />
    </div>
</%def>
<%def name="sidenav()">
<h1>${_('What is OpenID?')}</h1>

<p>${_('Its a single username and password that allows you to log in to any OpenID-enabled site.')}</p>

<p>${_('It works on thousands of websites.')}</p>

<p>${_('Its an open standard.')}</p>

<p>${_('And we are too lazy to implement our own login process. Which is good, because this way we cant mess it up.')}</p>

<ul>
    <li><a href="http://openid.net/what/">${_('learn more')}</a></li>
    <li><a href="http://openid.net/get/">${_('get one')}</a></li>
</ul>
</%def>
