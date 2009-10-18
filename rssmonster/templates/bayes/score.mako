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

<h2>tokens</h2>
% for word in c.tokens:
${word}, 
% endfor

${c.tokens}

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

</%def>

