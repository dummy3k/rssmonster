"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from webhelpers.pylonslib import Flash as _Flash
from routes import url_for

flash = _Flash()

def dump(v):
#    return 'Hello World'
#    return str(dir(v))
    html = "<p><b>Dir() </b> %s</p>" % str(dir(v))

    try:
        for k in v.keys():    
            html +="<p><b>%s =</b> %s</p>" % (k,v[k])
    except AttributeError:
        pass
                
    return html


