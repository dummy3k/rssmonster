<%inherit file="/layout-default.mako"/>\
<%import rssmonster.lib.helpers as h %>

<%def name="title()">Add feed</%def>

<%def name="content()">

 <form id="signin-form" method="post" action="${h.url_for(action='add', id=None)}">
    <input type="text" name="url" />
    <input type="submit" value="Add" />
 </form>
 
</%def>

