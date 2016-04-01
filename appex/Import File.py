# coding: utf-8

# https://gist.github.com/Gerzer/2e9e421ccdd38155b357

import appex
import os
import shutil

def main():
	if not appex.is_running_extension():
		print 'ERROR: This script is meant to be run from the sharing extension.'
	else:
		input_files = appex.get_attachments()
		for input_file in input_files:
			head, tail = os.path.split(input_file)
			shutil.copy(input_file, tail)

if __name__ == '__main__':
	main()