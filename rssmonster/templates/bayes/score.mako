<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Score for '${c.entry.title}'</%def>

<%def name="content()">

<table>
    <tr><th>Spam Score</th><td>${c.score}&nbsp;</td></tr>
    <tr><th>Is_spam</th><td>${c.is_spam}&nbsp;</td></tr>
    <tr>
        <th>Link</th>
        <td><a href="${c.entry.link}" target='_blank'/>${c.entry.link}&nbsp;</a></td>
    </tr>
    <tr><th>Updated</th><td>${c.entry.updated}&nbsp;</td></tr>
</table>

Feed:
<%namespace name='feed_actions' file='/feed/feed_actions.mako' />
${feed_actions.render(c.feed)}

Entry:
% for x in c.entry.actions(url.current(), c.user):
<a href="${x['link']}">${x['title']}</a>&nbsp;
% endfor

<h2>summary</h2>
${h.strip_ml_tags(c.entry.summary)}

<h2>tokens</h2>
% for word in c.tokens:
%   if word in map(lambda x: x[0], c.pool_data_spam) or word in map(lambda x: x[0], c.pool_data_ham):
<b>
%   endif
${word | h} 
%   if word in map(lambda x: x[0], c.pool_data_spam) or word in map(lambda x: x[0], c.pool_data_ham):
<a href="${h.url_for(controller='bayes', action='mark_stopword', id=c.feed.id, word=word, return_to=url.current())}"/>x</a></b>
%   endif
,
% endfor


<div class="leftside">
<h2>Spam words</h2>
% for word, cnt in c.pool_data_spam:
%   if word in c.tokens:
<b>
%   endif
${word} (${cnt}), 
%   if word in c.tokens:
<a href="${h.url_for(controller='bayes', action='mark_stopword', id=c.feed.id, word=word, return_to=url.current())}"/>x</a></b>
</b>
%   endif
% endfor
</div>

<div class="rightside">
<h2>Ham words</h2>
% for word, cnt in c.pool_data_ham:
%   if word in c.tokens:
<b>
%   endif
${word} (${cnt}), 
%   if word in c.tokens:
<a href="${h.url_for(controller='bayes', action='mark_stopword', id=c.feed.id, word=word, return_to=url.current())}"/>x</a></b>
</b>
%   endif
% endfor
</div>

</%def>

