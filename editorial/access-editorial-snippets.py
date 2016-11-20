# https://forum.omz-software.com/topic/3532/snippets-access-to-back-up/12

# Try this on editorial. You can do cut-and-paste. (Or you can write your own import/export based on this code.) May be there are better ways.

# coding: utf-8

import os, glob

for f in glob.glob('../Snippets/*.snpt'):
	print('\n%s\n'%f + open(f).read() + '\n')

#Code printing snippet name instead of uuid

# coding: utf-8

import os, json, glob

with open('../Snippets/Snippets.edcmd') as fp:
	json_obj = json.load(fp)
	
snippet_dict = {}
for i in json_obj:
	snippet_dict[i['uuid']] = i['title']
	
#print(snippet_dict)
for f in glob.glob('../Snippets/*.snpt'):
	fuuid = (f.split('/')[-1]).split('.')[0]
	fname = snippet_dict[fuuid]
	with open(f) as fp:
		print('#####################')
		print('#'+fname+':')
		print(fp.read())
		print('#####################')

