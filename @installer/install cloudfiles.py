# https://gist.github.com/omz/9c54a36c619261067225
modname = 'cloudfiles'
base_url = 'https://raw.github.com/rackspace/python-cloudfiles/master/cloudfiles/'
files = ['__init__.py', 'authentication.py', 'connection.py', 'consts.py',
         'container.py', 'errors.py', 'fjson.py', 'storage_object.py',
         'utils.py']

import os
import requests

print 'Creating module directory:', modname
if not os.path.isdir(modname):
	os.mkdir(modname)

for filename in files:
	print 'Downloading', filename
	url = base_url + filename
	r = requests.get(url)
	dest = os.path.join(modname, filename)
	with open(dest, 'w') as f:
		f.write(r.text)
print 'Done.'
