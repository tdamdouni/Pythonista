import argparse
import re
from sys import argv
from urllib import quote
import webbrowser

def search_and_replace(data_string, old, new, count=0, flags=0):
	substitute = re.sub(old, new, data_string, count, flags)
	drafts_call = 'drafts4://x-callback-url/create?text={0}'.format(quote(substitute))
	webbrowser.open(drafts_call)

def parse_input(data):
	'''Parse input from Drafts command-line-like.'''
	parser = argparse.ArgumentParser(description='Search and Replace for Drafts.')
	
	parser.add_argument('datastring',
	                    metavar='STRING',
	                    nargs='*',
	                    help='the string to search in')

	parser.add_argument('-old', '--old',
                      metavar='STRING|REGEXP',
                      dest='old',
                      help='the old string. regular expression allowed.')

	parser.add_argument('-new', '--new',
	                    metavar='STRING',
	                    dest='new',
	                    help='the new string to replace with.')

	parser.add_argument('-c', '--c', '-count', '--count',
	                    metavar='INT',
	                    default=0,
	                    dest='count',
	                    help='the number of times to replace.')

	# Possible inputs for flags:
	# 2 = IGNORECASE
	# 4 = LOCALE
	# 8 = MULTILINE
	# 16 = DOTALL
	# 64 = VERBOSE
	# May be summed.
	parser.add_argument('-f', '--f', '-flags', '--flags',
	                    metavar='INT|re.FLAG',
	                    default=0,
	                    dest='flags',
	                    help='the flags for regeular expression substitution.')
	                    
	args = parser.parse_args(data)
	search_and_replace(' '.join(args.datastring), args.old, args.new, int(args.count), int(args.flags))

if __name__ == '__main__':
	parse_input(argv[1].split(' '))