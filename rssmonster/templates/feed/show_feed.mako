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

% for x in c.feed.actions(h.url_for(), c.user):
<a href="${x['link']}">${x['title']}</a>&nbsp;
% endfor


<p>${c.page.pager()}</p>

<%namespace name='entry_mako' file='entry.mako' />
<div style="max-width:45%;float:left;">
<h2>Lastest Sapm</h2>
% for e in c.last_spam_entries:
${entry_mako.entry(e)}
% endfor
</div>

<div style="max-width:45%;float:right;">
<h2>Lastest Ham</h2>
% for e in c.last_ham_entries:
${entry_mako.entry(e)}
% endfor
</div>

<span style="float:clear;">
<h2>Lastest Entries</h2>
<p>${c.page.pager()}</p>
<table border=1>
    <tr>
        <th>${_('id')}</th>
        <th>${_('title')}</th>
        <th>${_('Spam')}</th>
        <th>${_('Ham')}</th>
        <th>&nbsp;</th>
    </tr>

    % for entry in c.page.items:
    <tr class='${h.iif(entry.is_spam, "spam", "")}'>
        <td><a name="${entry.id}" id="${entry.id}">${entry.id}</a></td>
        <td>
            <a href='${entry.link}' class='${h.iif(entry.is_spam, "spam", "")}'>${entry.title}</a>
            <p>${h.strip_ml_tags(entry.summary)}</p>
        </td>
        <td>${entry.score['spam']}</td>
        <td>${entry.score['ham']}</td>
        <td>
            % for x in entry.actions(h.url_for() + '#' + str(entry.id), c.user):
            <a href="${x['link']}">${x['title']}</a>&nbsp;
            % endfor
        </td>
    </tr>
    %endfor

</table>
<p>${c.page.pager()}</p>
</span>


</%def>

