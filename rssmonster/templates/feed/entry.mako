<%def name="entry(e)">

<div style='max-width:100%;white-space:nowrap;clear:both'>
    <div style='max-width:60%;width:80%;overflow:hidden;float:left;'>
        <a style='max-width:100%;overflow:hidden;float:left;' href="${e.link}"}'>
            ${e.title}</a>
    </div>
    <div style='float:right;text-align:right;'>
    % for x in e.actions(h.url_for(), c.user):
        <a href="${x['link']}">${x['title']}</a>&nbsp;
    % endfor
    </div>
</div>

</%def>
