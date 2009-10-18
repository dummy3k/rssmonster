"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from webhelpers.pylonslib import Flash as _Flash
from routes import url_for
from webhelpers.html.converters import markdown

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

    html += "<h1>Dict</h1>"
    for k in dir(v):
        try:
            html +="<p><b>%s =</b> %s</p>" % (k,v[k])
        except KeyError:
            pass    
        except TypeError:
            pass    
                
    html += "<h1>__Dict__</h1>"
    for k in dir(v):
        try:
            html +="<p><b>%s =</b> %s</p>" % (k,v.__dict__[k])
        except KeyError:
            pass    
                
    return html

def iif(expr, a, b):
    if expr:
        return a
    else:
        return b


