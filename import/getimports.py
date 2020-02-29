#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List names of all imports in all Python files given on command line."""
from __future__ import print_function

import sys
import ast


NODE_TYPES = (ast.Import, ast.ImportFrom)


def get_imports(source):
	tree = ast.parse(source)
	
	for node in ast.walk(tree):
		if isinstance(node, NODE_TYPES):
			lineno = getattr(node, 'lineno', None)
			if isinstance(node, ast.Import):
				mods = [a.name for a in node.names]
			else:
				mods = [node.module]
			yield (lineno, node, mods)
			
if __name__ == '__main__':
	for fn in sys.argv[1:]:
		with open(fn) as fp:
			try:
				for lineno, node, mods in get_imports(fp.read()):
					print("{}:{}:{}".format(fn, lineno, ", ".join(mods)))
			except:
				print("Could not parse '{}'.".format(fn))
				import traceback
				traceback.print_exc()

