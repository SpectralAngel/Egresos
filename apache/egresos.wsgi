# -*- coding: utf-8 -*-
import sys
from os import path
program, subplace = path.split(path.dirname(__file__))
sys.path.append(program)
sys.path.append(path.join(program, 'wording'))
sys.stdout = sys.stderr
import os

locale_name = None
if os.name == 'nt':
    locale_name = 'Spanish_Honduras.1252'
else:
    locale_name = "es_HN.utf8"

import os
os.environ['PYTHON_EGG_CACHE'] = program

import atexit
import cherrypy
import cherrypy._cpwsgi
import turbogears
import locale
locale.setlocale(locale.LC_ALL, locale_name)

turbogears.update_config(configfile="dev.cfg", modulename="egresos.config")
turbogears.config.update({'global': {'server.environment': 'development'}})
turbogears.config.update({'global': {'autoreload.on': False}})
turbogears.config.update({'global': {'server.log_to_screen': False}})

import egresos
from egresos import controllers

cherrypy.root = controllers.root.Root()

if cherrypy.server.state == 0:
    atexit.register(cherrypy.server.stop)
    cherrypy.server.start(init_only=True, server_class=None)

application = cherrypy._cpwsgi.wsgiApp
