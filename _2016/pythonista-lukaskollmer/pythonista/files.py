# https://github.com/lukaskollmer/pythonista

"""
Use this module to access and modify the /Documents folder
"""

__author__ = "Lukas Kollmer<lukas.kollmer@gmail.com>"
__copyright__ = "Copyright (c) 2016 Lukas Kollmer<lukas.kollmer@gmail.com>"

import os

from pythonista import defaults


def get_recents():
	files = defaults.get("RecentFiles")
	return list(map(str, files))

def clear_recents():
	defaults.set("RecentFiles", ns([]))

def list_all(path="~/Documents", depth=1):
	full_path = os.path.expanduser(path)
	files_in_dir = {}
	for root, dirs, files in os.walk(full_path):
		
		root_path_items = root.replace(full_path, "").split("/")
		root_path_items.pop(0)
		
		"""print("Root:", root)
		print("Root path items:", root_path_items)
		print("Dir:", dirs)
		print("Files:", files)
		print("\n"*3)"""
		
		_files = files_in_dir
		length = len(root_path_items)
		for index, path_item in enumerate(root_path_items):
			#print(index, path_item, length)
			if not (index + 1) == length:
				if not path_item in _files:
					_files[path_item] = {}
				_files = _files[path_item]
			else:
				_files["__files__"] = files
	return files_in_dir
				

def search(term, dir="~/Documents", filename=True):
	dir = os.path.expanduser(dir)
	if filename:
		return [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir) for f in filenames if term.lower() in f.lower()]
	else:
		return [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir) for f in filenames if term.lower() in os.path.join(dp, f).replace(dir, "").lower()]
	


if __name__ == "__main__":
	import console
	console.clear()
	#print(list_all(depth=1000))
	print(search("main"))
