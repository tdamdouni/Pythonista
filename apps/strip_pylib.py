# https://forum.omz-software.com/topic/3691/preparation-for-xcode-delete-files-in-pythonistaapptemplate/13

# Clear all
# To get pythonista to work again, restart the app
import sys
sys.modules[__name__].__dict__.clear()

# Now import
import sys
import inspect
import importlib

splitstr = "PythonistaKit.framework"

pyt_mods = [
        "os",
        "datetime",
        "json",
        "requests",
        "operator",
        "time",
        ]

pythonista_mods = [
        "ui",
        "console",
        "dialogs",
        "objc_util"
      ]

all_mods = pyt_mods + pythonista_mods

keep_list = []
for imods in all_mods:
	try:
		m  = importlib.import_module(imods)
		dirpath, filepath = inspect.getfile(m).split(splitstr)
		keep_list.append(filepath)
		
	except TypeError as e:
		#print(e)
		pass
		
# Get the imported modules
dict = sys.modules
for key in dict:
	val = dict[key]
	if val == None:
		continue
	else:
		try:
			filepath = inspect.getfile(val)
			if splitstr in filepath:
				filepath_append = filepath.split(splitstr)[1]
				keep_list.append(filepath_append)
			else:
				pass
				
		except TypeError as e:
			#print(e)
			pass
			
# Make uniq and sort
keep_list = sorted(set(keep_list))

# Now find all files
import os

fp = dirpath+splitstr
extensions = [".py", ".pyo"]
all_files = []
for path, dirs, files in os.walk(fp):
	for f in files:
		filename, file_extension = os.path.splitext(f)
		if "/pylib/" in path or "/pylib_ext/" in path:
			if file_extension in extensions:
				stringfp = os.path.join(path, f)
				dirpath, filepath = stringfp.split(splitstr)
				all_files.append(filepath)
				
# Make uniq and sort
all_files = sorted(set(all_files))

# Make a delete list
dellist = [x for x in all_files if x not in keep_list]

# Write delete file
fname = 'pylib_clean.sh'
f = open(fname,'w')
f.write("#!/usr/bin/env bash\n")

for idel in dellist:
	f.write("rm ."+idel+"\n")
f.close()

f = open(fname, "r")
for line in f:
	print(line),
f.close()

