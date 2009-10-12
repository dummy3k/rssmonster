<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">All feeds</%def>

<%def name="content()">
<table border=1>
    <tr>
        <th>${_('id')}</th>
        <th>${_('title')}</th>
        <th>${_('url')}</th>
        <th>${_('last_update')}</th>
        <th>&nbsp;</th>
    </tr>

    % for feed in c.feeds:
    <tr>
        <td>${feed.id}</td>
        <td>${feed.title}</td>
        <td>${feed.url}</td>
        <td>${feed.last_update}</td>
        <td>
            <a href='${h.url_for(action='show', id=feed.id)}'>${_('Show')}</a>&nbsp;
            <a href='${h.url_for(action='delete')}'>${_('Delete')}</a>
       </td>
    </tr>
    %endfor

</table>
</%def>

