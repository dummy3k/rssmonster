${c.entry.summary}

% if c.entry.is_spam:
<a href='${h.url_for(controller='bayes', action='mark_as_ham', id=c.entry.id)}'>${_('No Spam')}</a>&nbsp;
% else:
<a href='${h.url_for(controller='bayes', action='mark_as_spam', id=c.entry.id)}'>${_('Spam')}</a>&nbsp;
% endif
