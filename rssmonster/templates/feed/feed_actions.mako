<%def name="render(feed)">
<a href="${h.url_for(controller='feed', action='show_feed', id=feed.id)}"/>Summary</a>
<a href="${h.url_for(controller='feed', action='show_record', id=feed.id)}"/>Record</a>
<a href="${h.url_for(controller='feed', action='update', id=feed.id, return_to=url.current())}"/>Update</a>
<a href="${h.url_for(controller='bayes', action='show_guesser', id=feed.id)}"/>Guesser</a>
<a href="${h.url_for(controller='bayes', action='redo', id=feed.id, return_to=url.current())}"/>Redo</a>
</%def>

