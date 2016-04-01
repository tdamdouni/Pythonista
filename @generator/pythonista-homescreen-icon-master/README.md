https://forum.omz-software.com/topic/1358/pythonista-homescreen-icon-customizable-icons-for-your-scripts

pythonista-homescreen-icon
==========================

A Pythonista utility (meant to be put in the action menu) that allows you to add a home screen icon for any script


Installation script:

```python
import zipfile, requests, io

c = requests.request('GET', 'https://github.com/0942v8653/pythonista-homescreen-icon/archive/master.zip').content
with io.BytesIO() as b:
	b.write(c)
	with zipfile.ZipFile(b) as z:
		z.extractall()
```

Once it's installed, add the chooseicon.py file to the action menu. and give it a nice name.

Currently only tested on iPhone 5s, but it may work on iPhone 4/4s/6.