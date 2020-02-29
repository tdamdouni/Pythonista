from __future__ import print_function
# just some random utilities used during test & development

import os

#print os.listdir('.')
print(os.listdir('rooms'))

for i in range(7,13):
	fname = "rooms/%i.json.py" % i
	with open(fname, 'w') as f:
		f.write('')
	
