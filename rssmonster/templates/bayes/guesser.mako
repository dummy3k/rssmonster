<%inherit file="/layout-default.mako"/>
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Bayes details for '${c.feed.title}'</%def>

<%def name="content()">

##${str(c.pool_data)}

<div>
<%namespace name='feed_actions' file='/feed/feed_actions.mako' />
${feed_actions.render(c.feed)}
</div>

<h2>Stop words</h2>
% for word in c.stopwords:
${word.word}, 
% endfor

<div class="leftside">
<h2>Spam words</h2>
% for word, cnt in c.pool_data_spam:
${word}&nbsp;(${cnt} <a href="${h.url_for(controller='bayes', action='mark_stopword', word=word, return_to=h.url_for())}"/>x</a>), 
% endfor
</div>

<div class="rightside">
<h2>Ham words</h2>
% for word, cnt in c.pool_data_ham:
${word}&nbsp;(${cnt}&nbsp;<a href="${h.url_for(controller='bayes', action='mark_stopword', word=word, return_to=h.url_for())}"/>x</a>), 
% endfor
</div>

</%def>

