"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from webhelpers.pylonslib import Flash as _Flash
from routes import url_for
import re
from datetime import datetime, timedelta
#from webhelpers.html.converters import markdown

#http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/feedgenerator/
# Atom1Feed:
#   - does not support feed description(?)
from webhelpers.feedgenerator import Rss201rev2Feed as DefaultFeed

flash = _Flash()

def dump(v):
    html = "<p><b>str() </b> %s</p>" % str(v)
    html += "<p><b>Dir() </b> %s</p>" % str(dir(v))

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
        except AttributeError:
            pass

    return html

def iif(expr, a, b):
    if expr:
        return a
    else:
        return b


def go_back(default = '/'):
    """ return to the original source """
    from pylons import request
    from pylons.controllers.util import redirect

    if request.params.get('return_to'):
        return redirect(request.params.get('return_to'))

    return redirect(default)

# taken from http://code.activestate.com/recipes/440481/
def strip_ml_tags(in_text):
    """Description: Removes all HTML/XML-like tags from the input text.
    Inputs: s --> string of text
    Outputs: text string without the tags

    # doctest unit testing framework

    >>> test_text = "Keep this Text <remove><me /> KEEP </remove> 123"
    >>> strip_ml_tags(test_text)
    'Keep this Text  KEEP  123'
    """

    if not in_text:
        return None

    # convert in_text to a mutable object (e.g. list)
    s_list = list(in_text)
    i,j = 0,0

    while i < len(s_list):
        # iterate until a left-angle bracket is found
        if s_list[i] == '<':
            while i < len(s_list) and s_list[i] != '>':
                # pop everything from the the left-angle bracket until the right-angle bracket
                s_list.pop(i)

            if i < len(s_list):
                # pops the right-angle bracket, too
                s_list.pop(i)
        else:
            i=i+1

    # convert the list back into text
    join_char=''
    return join_char.join(s_list)

def age(x):
    if not x:
        return "never"

    from babel.dates import format_timedelta
    from datetime import datetime

    return format_timedelta(datetime.now()-x, locale='en_US')

def timedelta_from_string(s):
    m = re.match('(\d+)(\w)', s)

    if m.group(2) == 'm':
        return timedelta(minutes=int(m.group(1)))

    if m.group(2) == 'h':
        return timedelta(hours=int(m.group(1)))

    if m.group(2) == 'd':
        return timedelta(days=int(m.group(1)))

    if m.group(2) == 'w':
        return timedelta(days=int(m.group(1)*7))


def find(f, data):
    #x.feed_id==feed_data.id
    reduce(lambda x,y:h.iif(f(x),x,y), c.rss_user.bayes_feed_settings)
