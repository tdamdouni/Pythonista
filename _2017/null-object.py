# https://forum.omz-software.com/topic/4305/crash

import gc
for i, obj in enumerate(gc.get_objects()):
	t = repr(obj)
	if 'NULL' in t and isinstance(obj, tuple):
		print(i, t)
#       print('...', obj[0])  # crashes
print(i, 'total')

