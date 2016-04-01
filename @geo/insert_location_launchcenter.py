# -*- coding: utf-8 -*-

# To call script, use the follwing URL Action:
# - <pythonista://insert_location.py?action=run&argv=nav>

import location
import urllib
import webbrowser
import time
import clipboard

location.start_updates()
time.sleep(1)
b = location.get_location()
location.stop_updates()

b = str(b["latitude"]) + "," + str(b["longitude"]) + ","

clipboard.set(b)

webbrowser.open("launch://x-callback-url/")
