# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/45c4f891f059bbcc38e0

# https://forum.omz-software.com/topic/2784/feature-request-pythonista-built-in-file-picker

"""A set of operations for working with the file lists returned from zipfile.ZipFile.namelist()"""
from __future__ import print_function

import os

def getParentDirs(path):
	""" "test/again/hello" -> ["test", "test/again"] """
	dirs = path.split("/")[:-1]
	if dirs:
		return ["/".join(dirs[:i+1]) for i,d in enumerate(dirs) if dirs[:i+1]]
	else:
		return []
		
def getAllDirNames(filelist):
	"""["a/b.py","b/c.py","a/b/c.py"] -> ["a","b","a/b"]"""
	dirs = set([os.path.split(d)[0] for d in filelist])
	for d in list(dirs):
		for pd in getParentDirs(d):
			dirs.add(pd)
	return sorted([d for d in list(dirs) if d])
	
def depth(path):
	"""a/b/c -> 3; a/b/c/d -> 4"""
	return path.count("/")+1
	
def getSubDirs(filelist,path):
	"""["a/b/c.py","a/c/d.py"], a -> [b,c]"""
	dirs=getAllDirNames(filelist)
	return [d for d in dirs if d.startswith(path) and d!=path and depth(d)==depth(path)+1]
	
def getSubFiles(flst, path):
	"""["a/b.py", "a/c.py"], a -> ["a/b.py", "a/c.py"]"""
	return [d for d in flst if d.startswith(path) and d!=path and depth(d)==depth(path)+1]
	
def allSubFiles(flst, path):
	return [d for d in flst if d.startswith(path) and d!=path]
	
def isdir(flist, path):
	"""Whether the path is a directory in file list `flist`"""
	return path in getAllDirNames(flist)
	
def isfile(flist, path):
	"""Whether the path is a file in file list `flist`"""
	return path in flist
	
def exists(flist, path):
	"""Whether the path is either a file or a directory in file list `flist`"""
	return isfile(flist,path) or isdir(flist,path)
	
if __name__ == "__main__":
	import zipfile
	files=zipfile.ZipFile("example.zip").namelist()
	print(getSubDirs(files, 'GitHub'))
	print(getSubFiles(files, 'GitHub'))

