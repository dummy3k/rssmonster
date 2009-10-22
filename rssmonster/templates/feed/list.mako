<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">All feeds</%def>

<%def name="content()">

<table>
    <tr>
        <th>${_('id')}</th>
        <th>${_('entries')}</th>
        <th>${_('title')}</th>
        <th>${_('last_fetch')}</th>
        <th>${_('last_builddate')}</th>
        <th>${_('updated')}</th>
        <th>${_('language')}</th>
        <th>&nbsp;</th>
    </tr>

    % for feed in c.feeds:
    <tr>
        <td>${feed.id}</td>
        <td>${len(feed.entries)}</td>
        <td>
            <a href ='${h.url_for(controller="feed", action="show_feed", id=feed.id)}'>
                ${feed.title}</a>
        </td>
        <td>${feed.last_fetch}</td>
        <td>${feed.last_builddate}</td>
        <td>${feed.updated}</td>
        <td>${feed.language}</td>
        <td>
            <%namespace name='feed_actions' file='feed_actions.mako' />
            ${feed_actions.render(feed)}
        </td>
    </tr>
    %endfor
</table>

</%def>

