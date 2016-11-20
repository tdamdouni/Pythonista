# https://forum.omz-software.com/topic/3316/pythonista-and-pycharm/9

import inspect, sound
fmt = '{} {}:\n    pass  #  {}\n'
for name, func in inspect.getmembers(sound):
	if callable(func):
		def_or_class = 'def' if 'function' in str(func) else 'class'
		print(fmt.format(def_or_class, name, func))

