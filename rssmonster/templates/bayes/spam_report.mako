<%namespace name='feed_actions' file='/feed/feed_actions.mako' />
## ${feed_actions.render(c.feed)}

<table>
%for entry in c.entries:
<tr>
<td><a href="${entry.link}">${entry.title}</a></td>

<td>
% for x in entry.actions(h.url_for(), c.rss_user):
<a href="${c.baseurl + x['link']}">${x['title']}</a>&nbsp;
% endfor
</td>

</tr>
%endfor

</table>
