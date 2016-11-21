import cloud

cloud.Import('pythonista.editor')
cloud.Import('Gestures')

pythonista.editor.WebTab().present()
g = Gestures.Gestures()
--------------------
DOCS_DIR = os.path.expanduser('~/Documents/')
SITE_DIR = os.path.join(DOCS_DIR, 'site-packages/')
--------------------
import json

with open("modules.json", "r") as f:
	modules = json.load(f)
--------------------
import requests

modules = requests.get("https://example.com/modules.json").json
--------------------

