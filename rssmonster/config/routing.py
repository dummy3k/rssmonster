"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller='feed', action='show_list')

    map.connect('/add', controller='feed', action='add')
    map.connect('/list', controller='feed', action='show_list')
    map.connect('/feed/{id}', controller='feed', action='show_feed')
    map.connect('/feed/{id}/page/{page}', controller='feed', action='show_feed')
    map.connect('/feed/{id}/ignore/{word}', controller='bayes', action='mark_stopword')
    map.connect('/feed/{id}/unignore/{word}', controller='bayes', action='unmark_stopword')
    map.connect('/signout', controller='login', action='signout')
    map.connect('/user/{user_id}/{controller}/{action}/{id}')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/')
    map.connect('/{controller}/{action}/{id}')
    map.connect('/{controller}/', action='index')


    return map
