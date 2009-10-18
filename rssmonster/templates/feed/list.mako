<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">All feeds</%def>

<%def name="content()">
<table border=1>
    <tr>
        <th>${_('id')}</th>
        <th>${_('entries')}</th>
        <th>${_('title')}</th>
        <th>${_('url')}</th>
        <th>${_('last_fetch')}</th>
        <th>${_('last_builddate')}</th>
        <th>${_('updated')}</th>
        <th>${_('language')}</th>
        <th>&nbsp;</th>
    </tr>

    % for feed in c.feeds:
    <tr>
        <td>${feed.id}</td>
        <td>${feed.get_entry_count()}</td>
        <td>
            <a href ='${feed.link}'><img src='${feed.image}' width='16px' height='16px' /> ${feed.title}</a>
            <p>${feed.subtitle}</p>
        </td>
        <td>${feed.url}</td>
        <td>${feed.last_fetch}</td>
        <td>${feed.last_builddate}</td>
        <td>${feed.updated}</td>
        <td>${feed.language}</td>
        <td>
            <a href='${h.url_for(action='show_feed', id=feed.id)}'>${_('Show')}</a>&nbsp;
            <a href='${h.url_for(action='update', id=feed.id, return_to=h.url_for())}'>${_('Fetch')}</a>&nbsp;
            <a href='${h.url_for(controller='bayes', 
                action='redo', id=feed.id, return_to=h.url_for(controller='bayes', action='show_score', id=feed.id))}'>${_('ReDo')}</a>&nbsp;
##            <a href='${h.url_for(action='rss', id=feed.id)}'>${_('Rss')}</a>&nbsp;
##            <a href='${h.url_for(action='delete')}'>${_('Delete')}</a>
       </td>
    </tr>
    %endfor

</table>
</%def>

