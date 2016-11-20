# -*- coding: utf-8 -*-
"""Parse Python source code and get or print docstrings."""

__all__ = ('get_docstrings', 'print_docstrings')

import ast

from itertools import groupby
from os.path import basename, splitext


NODE_TYPES = {
    ast.ClassDef: 'Class',
    ast.FunctionDef: 'Function/Method',
    ast.Module: 'Module'
}


def get_docstrings(source):
	"""Parse Python source code and yield a tuple of ast node instance, name,
	line number and docstring for each function/method, class and module.
	
	The line number refers to the first line of the docstring. If there is
	no docstring, it gives the first line of the class, funcion or method
	block, and docstring is None.
	
	"""
	tree = ast.parse(source)
	
	for node in ast.walk(tree):
		if isinstance(node, tuple(NODE_TYPES)):
			docstring = ast.get_docstring(node)
			lineno = getattr(node, 'lineno', None)
			
			if (node.body and isinstance(node.body[0], ast.Expr) and
			isinstance(node.body[0].value, ast.Str)):
				# lineno attribute of docstring node is where string ends
				lineno = node.body[0].lineno - len(node.body[0].value.s.splitlines()) + 1
				
			yield (node, getattr(node, 'name', None), lineno, docstring)
			
			
def print_docstrings(source, module='<string>'):
	"""Parse Python source code from file or string and print docstrings.
	
	For each class, method or function and the module, prints a heading with
	the type, name and line number and then the docstring with normalized
	indentation.
	
	The module name is determined from the filename, or, if the source is passed
	as a string, from the optional `module` argument.
	
	The line number refers to the first line of the docstring, if present,
	or the first line of the class, funcion or method block, if there is none.
	
	Output is ordered by type first, then name.
	
	"""
	if hasattr(source, 'read'):
		filename = getattr(source, 'name', module)
		module = splitext(basename(filename))[0]
		source = source.read()
		
	docstrings = sorted(get_docstrings(source),
	key=lambda x: (NODE_TYPES.get(type(x[0])), x[1]))
	grouped = groupby(docstrings, key=lambda x: NODE_TYPES.get(type(x[0])))
	
	for type_, group in grouped:
		for node, name, lineno, docstring in group:
			name = name if name else module
			heading = "%s '%s', line %s" % (type_, name, lineno or '?')
			print(heading)
			print('-' * len(heading))
			print('')
			print(docstring or '')
			print('\n')
			
			
if __name__ == '__main__':
	import sys
	
	with open(sys.argv[1]) as fp:
		print_docstrings(fp)

