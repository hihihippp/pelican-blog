#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Till Bergmann'
SITESUBTITLE = u"a blog on data stuff by Till Bergmann"
SITENAME = u"Paranormal Distributions"
SITEURL = 'http://www.tillbergmann.com/blog'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
GITHUB_ADDRESS = "https://github.com/tillbe"
EMAIL_ADDRESS = "tbergmann@ucmerced.edu"
TWITTER_ADDRESS = "http://twitter.com/till_be"
SHOW_ARTICLE_AUTHOR = False
# PROFILE_IMAGE_URL = "images/profile.png"
# MENUITEMS = [
# 		("CV", "http://www.tillbergmann.com/cv.html"),	
# ]

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)


# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

MARKUP = ('md')

READERS = {'html': None, # ignores html files in content
           'ipynb': None}

THEME = "crowsfoot"
PLUGIN_PATHS = ['pelican-plugins']

PLUGINS = [	'pelican-knitr',
            "render_math", 
            'liquid_tags.notebook',
            'pelican-bibtex']

STATIC_PATHS = ['pages','images', 'figure']

ARTICLE_URL = "articles/{slug}.html"
ARTICLE_SAVE_AS = "articles/{slug}.html"

PUBLICATIONS_SRC = 'content/pubs.bib'

# FILES_TO_COPY = (('content/pages/.htaccess', '.htaccess'))
OUTPUT_RETENTION = [".htaccess"]   
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
