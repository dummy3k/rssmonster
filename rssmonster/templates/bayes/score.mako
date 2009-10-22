<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Score for '${c.entry.title}'</%def>

<%def name="content()">

<table>
    <tr>
        <th>Spam Score</th>
        <td>${c.score}&nbsp;</td>
    </tr>
    <tr>
        <th>Is_spam</th>
        <td>${c.is_spam}&nbsp;</td>
    </tr>
</table>

Feed:
<%namespace name='feed_actions' file='/feed/feed_actions.mako' />
${feed_actions.render(c.feed)}

Entry:
% for x in c.entry.actions(h.url_for(), c.user):
<a href="${x['link']}">${x['title']}</a>&nbsp;
% endfor

<h2>summary</h2>
${c.entry.summary}
<h2>tokens</h2>
% for word in c.tokens:
${word | h}, 
% endfor


<div class="leftside">
<h2>Spam words</h2>
% for word, cnt in c.pool_data_spam:
%   if word in c.tokens:
<b>
%   endif
${word} (${cnt}), 
%   if word in c.tokens:
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
</b>
%   endif
% endfor
</div>

</%def>

