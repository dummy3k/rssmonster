<%inherit file="/layout-default.mako"/>
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Bayes details for '${c.feed.title}'</%def>

<%def name="content()">

##${str(c.pool_data)}

<div>
##<a href='${h.url_for(controller='bayes', action='redo', id=c.feed.id, return_to=h.url_for())}'>${_('ReDo')}</a>&nbsp;
% for x in c.feed.actions(h.url_for(), c.user):
<a href="${x['link']}">${x['title']}</a>&nbsp;
% endfor
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

