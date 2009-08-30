#!C:\Python25\python.exe
# -*- coding: utf-8 -*-
"""Start script for the Egresos TurboGears project.

This script is only needed during development for running from the project
directory. When the project is installed, easy_install will create a
proper start script.
"""

import sys
from egresos.commands import start, ConfigurationError
import locale

if __name__ == "__main__":
    try:
        locale.setlocale(locale.LC_ALL, "")
        print locale.getlocale()
        start()
    except ConfigurationError, exc:
        sys.stderr.write(str(exc))
        sys.exit(1)
