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

os.environ['PYTHON_EGG_CACHE'] = program

import turbogears
import locale
locale.setlocale(locale.LC_ALL, locale_name)

turbogears.update_config(configfile="dev.cfg", modulename="egresos.config")
turbogears.config.update({'global': {'server.webpath': '/egresos',
                                     'engine.start': False}})

from egresos import command

print(turbogears.config.get("server.webpath"))
application = command.start()
