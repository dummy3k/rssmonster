This file is for you to describe the rssmonster application. Typically
you would include information such as the information below:

Installation and Setup
======================

Install ``rssmonster`` using easy_install::

    easy_install rssmonster SQLAlchemy Pylons SQLAlchemy-migrate mock python-openid feedparser
    easy_install http://dl.getdropbox.com/u/530973/Reverend-0.3dev_r17655-py2.6.egg
    easy_install http://dl.getdropbox.com/u/530973/Babel-1.0dev_r0-py2.6.egg

Make a config file as follows::

    paster make-config rssmonster config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
