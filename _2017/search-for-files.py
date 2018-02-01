# https://forum.omz-software.com/topic/4495/search-for-files/6

import os
import fnmatch

def search_files(wordlist, directory,
      include_pattern=None, exclude_pattern=None):
	fnlist = []
	for dirpath, dirs, files in os.walk(directory):
		for filename in files:
			fname = os.path.join(dirpath, filename)
			to_include = True
			if exclude_pattern:
				if fnmatch.fnmatch(fname, exclude_pattern):
					to_include = False
			if include_pattern and to_include:
				if not fnmatch.fnmatch(fname, include_pattern):
					to_include = False
			if to_include:
				if are_all_words_in_file(fname, wordlist):
					fnlist.append(fname)
	return fnlist
	
def get_words(filename):
	with open(filename) as fp:
		for line in fp:
			for word in line.split():
				yield word
				
def are_all_words_in_file(filename, wordlist):
	return set(wordlist.split()).issubset(get_words(filename))
	
print (search_files('os class', '.', include_pattern="*.py"))

