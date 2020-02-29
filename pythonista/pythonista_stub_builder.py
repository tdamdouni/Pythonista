from __future__ import print_function
# https://github.com/amdescombes/pythonista_stub_builder

# pythonista_stub_builder: Creates python files for Pythonista builtin modules in order to use them with PyCharm to get code completion and resolve all import issues

import inspect
import sound
import _ui
import _scene2

default_indent = '    '
def_fmt = '\n\n%sdef %s():\n'
std_method_fmt = '\n%sdef %s(self):\n'
cls_method_fmt = '\n%sdef %s(cls):\n'
static_method_fmt = '\n%s@staticmethod'
class_fmt = '\n\n%sclass %s:\n'
doc_fmt = '    %s"""%s"""\n'
pass_fmt = '%s    pass\n'


def handle_attribute(name, func, indent):
	if isinstance(func, int) or isinstance(func, float):
		return '\n%s%s = %s\n' % (indent, name, func)
	else:
		return '\n%s%s = "%s"\n' % (indent, name, func)
		
		
def handle_function(name, func, indent, inclass):
	isfunc = 'function' in str(func)
	docstring = func.__doc__
	res = []
	if name != '__getattribute__':  # do nothing if it's a __getattribute__
		if inspect.isclass(func):  # it is a class
			if inclass:
				res.append(static_method_fmt % indent)
				res.append(std_method_fmt % (indent, name))
			else:
				res.append(class_fmt % (indent, name))
		elif inclass:
			if inspect.isbuiltin(func):  # to distiguish staticmethod and function
				res.append(static_method_fmt % indent)
				res.append(cls_method_fmt % (indent, name))
			else:
				if name in ['__format__', '__reduce_ex__', '__sizeof__', '__getslice__']:
					res.append(static_method_fmt % indent)
				res.append(std_method_fmt % (indent, name))
		else:
			res.append(def_fmt % (indent, name))
		if docstring:
			res.append(doc_fmt % (indent, docstring))
		res.append(pass_fmt % indent)
	return res, isfunc
	
	
def get_info(modul, indentlevel=0):
	_f = []
	indent = default_indent * indentlevel
	for name, func in inspect.getmembers(modul):
		if callable(func):
			res, isfunc = handle_function(name, func, indent, True)
			_f += res
		else:
			if name not in ['__doc__', '__name__', '__package__', '__dict__']:
				_f.append(handle_attribute(name, func, indent))
	return _f
	
	
def create_func(modul, modname, indentlevel=0):
	print("processing %s" % modname)
	_f = []
	indent = '    ' * indentlevel
	for name, func in inspect.getmembers(modul):
		if callable(func):
			res, isfunc = handle_function(name, func, indent, False)
			_f += res
			if inspect.isclass(func):
				cls = get_info(func, indentlevel + 1)
				_f += cls
		else:
			if name not in ['__doc__', '__name__', '__package__', '__dict__']:
				_f.append(handle_attribute(name, func, indent))
	open(modname, 'w').write(''.join(_f))
	print("processed %s" % modname)
	
	
if __name__ == "__main__":
	create_func(sound, 'sound.py')
	create_func(_ui, '_ui.py')
	create_func(_scene2, '_scene2.py')
	print("done")

