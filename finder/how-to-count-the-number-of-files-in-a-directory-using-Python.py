from __future__ import print_function
# _Captured: 2016-05-28 at 11:13 from [stackoverflow.com](http://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python)_

import os, os.path

# simple version for working with CWD
print(len([name for name in os.listdir('.') if os.path.isfile(name)]))

# path joining version for other paths
DIR = '/tmp'
print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))

#

import os

path, dirs, files = os.walk("/usr/lib").next()
file_count = len(files)

#

def directory(path,extension):
	list_dir = []
	list_dir = os.listdir(path)
	count = 0
	for file in list_dir:
		if file.endswith(extension): # eg: '.txt'
			count += 1
	return count
	
#

import os
print(len(os.listdir(os.getcwd())))

#

import fnmatch

print(len(fnmatch.filter(os.listdir(dirpath), '*.txt')))

#

import os
directory = 'mydirpath'

number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

#

import os
isfile = os.path.isfile
join = os.path.join

directory = 'mydirpath'
number_of_files = sum(1 for item in os.listdir(directory) if isfile(join(directory, item)))

#

def count_em(valid_path):
	x = 0
	for root, dirs, files in os.walk(valid_path):
		for f in files:
			x = x+1
	print("There are", x, "files in this directory.")
	return x
	
#

import os

list = os.listdir(dir) # dir is your directory path
number_files = len(list)
print(number_files)

#

import os

onlyfiles = next(os.walk(dir))[2] #dir is your directory path as string
print(len(onlyfiles))

#

import os

def count_files(in_directory):
	joiner= (in_directory + os.path.sep).__add__
	return sum(
	os.path.isfile(filename)
	for filename
	in map(joiner, os.listdir(in_directory))
	)
	
# >>> count_files("/usr/lib")

# >>> len(os.listdir("/usr/lib"))

#

import os
print(len(os.walk('/usr/lib').next()[2]))

#

import os
total_con=os.listdir('<directory path>')
files=[]
for f_n in total_con:
	if os.path.isfile(f_n):
		files.append(f_n)
print(len(files))

#

for root, dirs, files in os.walk(input_path):
	for name in files:
		if os.path.splitext(name)[1] == '.TXT' or os.path.splitext(name)[1] == '.txt':
			datafiles.append(os.path.join(root,name))
			
	print(len(files))
	
#

print(int(os.popen("ls | wc -l").read()))

