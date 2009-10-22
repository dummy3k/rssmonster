<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">${c.feed.title}</%def>

<%def name="content()">
<table border=1>
    <tr>
        <th>${_('id')}</th>
        <td>${c.feed.id}</td>
    </tr>
    <tr>
        <th>${_('title')}</th>
        <td>${c.feed.title}</td>
    </tr>
    <tr>
        <th>${_('summary')}</th>
        <td>${c.feed.subtitle}</td>
    </tr>
    <tr>
        <th>${_('url')}</th>
        <td>${c.feed.url}</td>
    </tr>
    <tr>
        <th>${_('last_fetch')}</th>
        <td>${c.feed.last_fetch}</td>
    </tr>
    <tr>
        <th>${_('last_builddate')}</th>
        <td>${c.feed.last_builddate}</td>
    </tr>
    <tr>
        <th>${_('updated')}</th>
        <td>${c.feed.updated}</td>
    </tr>
    <tr>
        <th>${_('language')}</th>
        <td>${c.feed.language}</td>
    </tr>
    <tr>
        <th>${_('entries')}</th>
        <td>${len(c.feed.entries)}</td>
    </tr>
</table>

<%namespace name='feed_actions' file='feed_actions.mako' />
${feed_actions.render(c.feed)}

</%def>

