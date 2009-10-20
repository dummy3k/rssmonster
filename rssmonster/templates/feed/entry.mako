<%def name="entry(e)">
<nobr><a href="${h.url_for(controller='bayes', action='show_score', id=e.id)}"}'>${e.title}</a></nobr>
##% for x in e.actions(h.url_for() + '#' + str(e.id), c.user):
##<a href="${x['link']}">${x['title']}</a>&nbsp;
##% endfor

</%def>
