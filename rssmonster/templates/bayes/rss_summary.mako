${c.entry.summary}

% for x in c.entry.actions(h.url_for(), c.rss_user):
<a href="${c.base_url}${x['link']}">${x['title']}</a>&nbsp;
% endfor
