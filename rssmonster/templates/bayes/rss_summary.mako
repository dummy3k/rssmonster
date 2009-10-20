${c.entry.summary}

% for x in c.entry.actions(h.url_for(), c.rss_user):
<a href="${x['link']}">${x['title']}</a>&nbsp;
% endfor
