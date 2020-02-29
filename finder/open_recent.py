#!python2

# https://gist.github.com/mcsquaredjr/5148002

'''Editor action to open recent files from the list'''
from __future__ import print_function

__date__ = '10-March-2013'
__author__ = 'mcsquaredjr'
__version__ = '0.1'

import os
import editor

# Length of the list
NUM_RECENT = 15

def get_input(mmax=NUM_RECENT):
	'Receive and validate the input'
	action = raw_input('\nEnter file number: ')
	try:
		action = int(action)
		if action < 1 or action > mmax:
			print('*** Cannot exceed {0:d}'.format(mmax))
			action = get_input()
	except ValueError:
		# Cannot convert to int
		print('*** Should be an integer between 1 and {0:d}'.format(mmax))
		action = get_input()
	return action

def all_files_under(path):
	'Iterates through *.py files under the given path.'
	for cur_path, dirnames, filenames in os.walk(path):
		for filename in filenames:
			if filename.endswith('.py'):
				yield os.path.join(cur_path, filename)

if __name__ == '__main__':
	# Get NUM_RECENT files 
	recent = sorted(all_files_under('.'), 
	                key=os.path.getmtime, 
	                reverse=True)[:NUM_RECENT]
	
	print('\n'*3)
	for i, fl in enumerate(recent):
		print('{:>15}\t{:<}'.format(i+1, fl))
	
	print(recent)
	num = get_input()
	# Open in editor
	editor.open_file(recent[num-1])
	print('=== Swipe right to switch to the editor.')
	
	
	

