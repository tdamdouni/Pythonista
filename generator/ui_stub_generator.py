# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2447/hackathon-challenge-set-by-ccc-started-new-thread/2

# https://gist.github.com/omz/dd8e999d4640db45bba4

# Hackathon Challange: write code that uses the Python inspect module to find all the functions and methods in the ui module and auto generate a ui.py file that has those same functions and modules stubbed out (with pass statement) such that an editor like sublime or PyCharm on Windoze or a real computer (e.g. Mac) will do autocompletion on all functions and methods of Pythonista ui code. All winning entries must 1) deliver correct code completion for all ui methods and functions, 2) pass all PyCharm PEP8 compliance tests (esp. line length) and 3) be posted in a GitHub repo by 8am Eastern time on Monday 14 Dec 2015 time. If there are multiple entries that pass the above tests then the shortest number of (nonblank) lines of code wins.

# Can you complete the challenge?!?

# Stub generator for ui module
# NOTES:
# * For classes, the base class is always assumed to be `object`. This isn't correct, but it shouldn't matter much because the
# generated stubs also contain inherited methods and data descriptors. Using the actual base classes would complicate things a
# little because the class definitions would have to appear in the correct order then.
# * It's not possible to get correct argspecs for functions and methods that are implemented in C, so they're always just
# `self, *args` (for bound methods) or `*args*` (for module-level functions) in the output.

from __future__ import print_function
import ui
import inspect
from numbers import Number

import console
console.clear()

from StringIO import StringIO

def write_constants(s, mod):
	members = inspect.getmembers(mod)
	s.write('# Constants:\n')
	for name, value in members:
		if isinstance(value, Number):
			s.write('%s = %s\n' % (name, value))
	s.write('\n')

def write_functions(s, mod):
	members = inspect.getmembers(mod)
	s.write('\n# Functions:\n')
	for name, value in members:
		if inspect.isfunction(value):
			s.write('def %s(*args):\n    pass\n' % (name,))
	s.write('\n')

def write_classes(s, mod):
	members = inspect.getmembers(mod)
	s.write('# Classes:\n')
	for name, value in members:
		if inspect.isclass(value):
			s.write('class %s (object):\n' % (name,))
			class_members = inspect.getmembers(value)
			s.write('    def __init__(self, *args):\n        pass\n')
			for m_name, m_value in class_members:
				if inspect.isdatadescriptor(m_value):
					s.write('        self.%s = None\n' % (m_name,))
			for m_name, m_value in class_members:
				if m_name.startswith('__'):
					continue
				elif inspect.ismethoddescriptor(m_value):
					s.write('    def %s(self, *args):\n        pass\n' % (m_name,))
				elif inspect.isbuiltin(m_value):
					s.write('    def %s(cls, *args):\n        pass\n' % (m_name,))
			s.write('\n')

def main():
	s = StringIO()
	write_constants(s, ui)
	write_functions(s, ui)
	write_classes(s, ui)
	mod_str = s.getvalue()
	print(mod_str)
	with open('ui_stubs.py', 'w') as f:
		f.write(mod_str)

if __name__ == '__main__':
	main()