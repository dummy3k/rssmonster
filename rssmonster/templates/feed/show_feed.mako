<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">${c.feed.title}</%def>

<%def name="content()">

##<p>${h.dump(c.feed)}</p>

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
        <td>${c.feed.get_entry_count()}</td>
    </tr>
</table>

<a href='${h.url_for(action='update', id=c.feed.id)}'>${_('update')}</a>&nbsp;

<h1>Lastest Entries</h1>

##${c.pagelist | n}


<table border=1>
    <tr>
        <th>${_('id')}</th>
        <th>${_('title')}</th>
        <th>${_('uid')}</th>
    </tr>

    % for entry in c.entries:
    <tr class='${h.iif(entry.is_spam, "spam", "")}'>
        <td>${entry.id}</td>
        <td>
            <a href='${entry.link}' class='${h.iif(entry.is_spam, "spam", "")}'>${entry.title}</a>
            <p>${h.markdown(entry.summary, safe_mode="remove")}</p>
            ${entry.is_spam}
        </td>
        <td>${entry.uid}</td>
    </tr>
    %endfor

</table>
</%def>

