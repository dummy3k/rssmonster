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
% for x in c.feed.actions(h.url_for(), c.user):
<a href="${x['link']}">${x['title']}</a>&nbsp;
% endfor

Entry:
% for x in c.entry.actions(h.url_for(), c.user):
<a href="${x['link']}">${x['title']}</a>&nbsp;
% endfor

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

