${c.entry.summary}

% if c.entry.is_spam:
<a href='${c.base_url}${h.url_for(controller='bayes', 
                                  action='mark_as_ham', 
                                  id=c.entry.id, 
                                  return_to=h.url_for(controller='bayes', action='show_score', id=c.entry.id))}'>${_('No Spam')}</a>&nbsp;
% else:
<a href='${c.base_url}${h.url_for(controller='bayes',
                                  action='mark_as_spam', 
                                  id=c.entry.id,
                                  return_to=h.url_for(controller='bayes', action='show_score', id=c.entry.id))}'>${_('Spam')}</a>&nbsp;
% endif
<a href='${c.base_url}${h.url_for(controller='bayes', action='show_score', id=c.entry.id)}'>${_('Score')}</a>&nbsp;

