<%inherit file="/layout-default.mako"/>
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Bayes details for '${c.feed.title}'</%def>

<%def name="content()">

##${str(c.pool_data)}

<div>
<%namespace name='feed_actions' file='/feed/feed_actions.mako' />
${feed_actions.render(c.feed)}
</div>

<div class="leftside">
<h2>Spam words</h2>
% for word, cnt in c.pool_data_spam:
${word} (${cnt}), 
% endfor
</div>

<div class="rightside">
<h2>Ham words</h2>
% for word, cnt in c.pool_data_ham:
${word} (${cnt}), 
% endfor
</div>

</%def>

