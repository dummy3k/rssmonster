<%namespace name='feed_actions' file='/feed/feed_actions.mako' />
## ${feed_actions.render(c.feed)}

%for entry in c.entries:
<a href="${h.url_for(controller='bayes', action='show_score', id=entry.id)}">${entry.title}</a><br>
%endfor
