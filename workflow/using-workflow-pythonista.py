# coding: utf-8

# Workflow & Pythonista

import urllib
import webbrowser

webbrowser.open('workflow://x-callback-url/run-workflow?name=PythonistaTest&input='+urllib.quote('Hi!'))

# pythonista://[[script name]]?action=run&argv=[[some argument to pass, can be a variable]]
