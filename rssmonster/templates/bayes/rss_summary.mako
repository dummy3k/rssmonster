${c.entry.summary |n}

% for x in c.entry.actions(h.url_for(controller='bayes', action='show_score', id=c.entry.id), c.rss_user):
<a href="${c.base_url}${x['link']}">${x['title']}</a>&nbsp;
% endfor
