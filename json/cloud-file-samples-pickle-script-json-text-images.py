# coding: utf-8

# https://forum.omz-software.com/topic/2840/cloud-file-samples-pickle-script-json-text-images/13

# coding: utf-8

# Cross Device Pickle
# Here is an example of doing a cross-device pickle between, for example, an iPad and an IPhone, using cloud.File (note: this requires the updated source that implements readline()).

from __future__ import print_function
import cloud, pickle

# on device 1

with cloud.File('', 'w', encryptionKey = 'password') as f:
	d = { "key1": "value1", "key2": "value2", "key3": "value3"}
	pickle.Pickler(f).dump(d)
	url = f.commit()
	
# on device 2

with cloud.File(url, 'r', encryptionKey = 'password') as f:
	d = {}
	d = pickle.Unpickler(f).load()
	print(d['key1'])
	print(d['key2'])
	print(d['key3'])
	
# ====================

parent = {'name': 'foo', 'children': []}
child = {'name': 'bar', 'parent': parent}
parent['children'].append(child)

json_str = json.dumps(parent) # This won't work

# ====================

# coding: utf-8

# Transfer script between devices
# Here is an example of using cloud.File to transfer a script between 2 devices, for example an iPad and an iPhone:

# cloudTransfer.py

import cloud, editor

script_to_share = editor.get_path()

# on device 1

with cloud.File('', 'w', encryptionKey = 'password') as f1:
	with open(script_to_share, 'r') as f2:
		f1.write(f2.read())
	url = f1.commit()
	
# on device 2
with cloud.File(url, 'r', encryptionKey = 'password') as f1:
	with open('TransferredScript.py', 'w') as f2:
		f2.write(f1.read())
editor.open_file('TransferredScript.py')

# ====================

# coding: utf-8

# Host JSON
# Here is an example of hosting JSON to replace the XML currently used in cloud.Import

# cloudJSON.py

import cloud, json

JSON = """
{
    "pythonista": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.app": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.editor": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "pythonista.console": "https://github.com/The-Penultimate-Defenestrator/Pythonista-Tweaks",
    "Gestures": "https://github.com/mikaelho/pythonista-gestures"
}
"""

#with cloud.File('', 'w') as f:
#   f.write(JSON)
#   url = f.commit()


with cloud.File('http://bit.ly/1XSmPCq', 'r') as f:
	print(json.load(f)['Gestures'])
	
# ====================

# coding: utf-8

# Transfer text between devices
# cloudText.py

import cloud, console

# on device 1

with cloud.File('', 'w', encryptionKey = 'password') as f:
	f.write('contents of encrypted file')
	url = f.commit()
	
# on device 2

with cloud.File(url, 'r', encryptionKey = 'password') as f:
	console.hud_alert(f.read())
	
# ====================

# coding: utf-8

# Transfer images between devices
# cloudInage.py

import cloud, ui
from PIL import Image

# on device 1

ip = Image.open('iob:ios7_cloud_outline_256')
with cloud.File('', 'wb', encryptionKey = 'password') as f:
	ip.save(f, ip.format)
	url = f.commit()
	
# on device 2

with cloud.File(url, 'rb', encryptionKey = 'password') as f:
	ui.Button(image = ui.Image.from_data(f.read())).present()
	
# ====================

