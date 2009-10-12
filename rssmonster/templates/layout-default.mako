<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <title>RSSmonster</title>

	<link href="/css/default.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="/css/ui-lightness/jquery-ui-1.7.2.custom.css" media="screen" rel="stylesheet" type="text/css" />
    <script src="/js/jquery-1.3.2.min.js" type="text/javascript"></script>
    <script src="/js/jquery-ui-1.7.2.custom.min.js" type="text/javascript"></script>
    <script src="/js/script.js" type="text/javascript"></script>
##    <script src="/config.js" type="text/javascript"></script>
##    <link rel="shortcut icon" href="/ico/logo.ico" type="image/x-icon">
##    <link rel="alternate" type="application/rss+xml" title="Wahrheitsmaschine: Neuste Thesen und Argumente" href="http://www.wahrheitsmaschine.de/latest-rss.xml" />
##    <link rel="alternate" type="application/rss+xml" title="Arguments for this thesis" href="http://www.wahrheitsmaschine.de/statement-43-rss.xml" />
</head>
<body>

    <a href="${h.url_for(controller='login', action='signout')}">Logout</a>
    <% flashes = h.flash.pop_messages() %>
    % if flashes:
        % for flash in flashes:
            <div class="ui-state-highlight ui-corner-all">
                <span class="ui-icon ui-icon-info">&nbsp;</span>
                <span class="flash-text">${flash}</span>
            </div>
        % endfor
    % endif

 <div class="main">
     ${self.content()}
 </div>
 
 <div class="sidenav">
  ${self.sidenav()}
 </div>
</body>
</html>

