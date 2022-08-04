#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jared Jennings'
SITENAME = u'Writing to think 2: Write harder'
# SITEURL = 'http://j.agrue.info'
# do not summarize
SUMMARY_MAX_LENGTH = None
DEFAULT_PAGINATION = 5

PATH = 'content'

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = u'en'

STATIC_PATHS = ['images', '']
IGNORE_FILES = ['.#*', '#*', '*~']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True



# for mg theme
#THEME = 'themes/mg'
