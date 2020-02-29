# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2506/possible-to-share-pyui-files_

from __future__ import print_function
print(open('Test.pyui').read())

###==============================

import clipboard

with open("thing.pyui") as f:
	clipboard.set(f.read())

