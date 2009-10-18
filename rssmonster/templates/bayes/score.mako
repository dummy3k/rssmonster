<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Score for '${c.entry.title}'</%def>

<%def name="content()">

<table>
    <tr>
        <th>Spam Score</th>
        <td>${c.entry.spam_score}&nbsp;</td>
    </tr>
    <tr>
        <th>Ham Score</th>
        <td>&nbsp;</td>
    </tr>

</%def>

