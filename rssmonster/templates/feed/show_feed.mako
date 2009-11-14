<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">${c.feed.title}</%def>

<%def name="content()">

%if c.feed.image:
<img src='${c.feed.image}' alt='logo' style='float:right;'/>
%endif
<a href ='${h.url_for(str(c.feed.link))}' target='_blank'>${c.feed.title}</a>
<p>${c.feed.subtitle}</p>

<%namespace name='feed_actions' file='feed_actions.mako' />
<p>${feed_actions.render(c.feed)}</p>

<form action="${h.url_for(controller='bayes', action='change_intervall', id=c.feed.id)}">
<p>
	Report spam every:
	<input type='text' name='word' value='${c.user.get_bayes_feed_setting(c.feed.id).summarize_at}'/>
	<input type='hidden' name='return_to' value='${h.url_for()}'/>
	<input type='submit' value='change'/>
</p>
</form>

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
        <td><a name="${entry.id}">${entry.id}</a></td>
        <td>${entry.updated}</td>
        <td>
            <a href='${entry.link}' class='${h.iif(entry.is_spam, "spam", "")}' target='_blank'>${entry.title}</a>
        </td>
        <td>${entry.score['spam'] and "%.4f" % entry.score['spam']}</td>
        <td>${entry.score['ham'] and "%.4f" % entry.score['ham']}</td>
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

