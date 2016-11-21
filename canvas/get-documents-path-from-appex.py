# coding: utf-8

# https://forum.omz-software.com/topic/2710/get-documents-path-from-appex/2
import os

os.path.expanduser("~/Documents")

#==============================

import os
docs_path = os.path.split(__file__)[0]

#==============================

import os

comps = __file__.split(os.sep)
doc_path = os.sep.join(comps[:comps.index('Documents')+1])

#==============================

def getPath():
	split=__file__.split('/')
	path=split[:split.index('Documents')+1]
	return '/'.join(path)

