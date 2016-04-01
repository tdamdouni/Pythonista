# -*- coding: utf-8 -*-
###############################################################################
# filenav_plugin for ShellistaExt
# http://github.com/dgelessus/pythonista-scripts/blob/master/filenav_plugin.py
# requires filenav by dgelessus (has to be importable, i. e. in PATH)
# http://github.com/dgelessus/pythonista-scripts/blob/master/filenav.py
# and ShellistaExt by briarfox
# http://github.com/briarfox/ShellistaExt
###############################################################################

from .. tools.toolbox import bash
import os.path

def main(line):
    try:
        import filenav
    except ImportError as err:
        print("Failed to load filenav: " + err.message)
        return
    print(list)
    b = bash(list)
    print(b)
    if b:
        filenav.run(b[0])
    else:
        filenav.run(os.path.fullpath("."))
