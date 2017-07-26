# coding: utf-8
# Olaf, Dec 2015, Pythonista 1.6 beta

# https://forum.omz-software.com/topic/2539/how-can-i-install-scapy/6

'''Appex GetFromURL
Pythonista app extension for use on share sheet of other apps to import file from URL into Pythonista
The file is saved at HOME/DESTINATION without user interaction (no 'save as' dialog) unless duplicate'''

from __future__ import print_function
try:
	import appex, console, contextlib, itertools, os, os.path, sys, time, urllib, urlparse
except ImportError:
	assert False, 'This script needs the appex module in Pythonista version > 1.5'
	
HOME, DESTINATION = 'Documents', 'FromURL' # you can change DESTINATION to any name of your liking

@contextlib.contextmanager
def callfunctionafterwardswithsec(function):
	'''Context-manager that calls function with duration of with block (sec) after termination
	
	>>> def pr_sec(sec): print('Duration {:3.2} sec'.format(sec))
	>>> with callfunctionafterwardswithsec(pr_sec): pass
	Duration 0.0 sec'''
	
	start = time.clock()
	yield
	end = time.clock()
	function(end - start)
	
def left_subpath_upto(path, sentinel):
	'''Left part (subpath) of path upto and including sentinel
	
	>>> print(left_subpath_upto('a/b/c', 'b'))
	a/b'''
	
	while path:
		head, tail = os.path.split(path)
		if tail == sentinel:
			break
		path = head
	return path
	
def iter_pad(length, arg0, *args):
	'''Iterator to pad arguments (at least 1) to specified length by repetition of final argument
	
	>>> print(''.join(iter_pad(3, 'a', 'b')))
	abb'''
	
	args = (arg0,) + args
	return itertools.islice(itertools.chain(args, itertools.repeat(args[-1])), length)
	
def parse_into_paths(input_url, HOME=HOME, DESTINATION=DESTINATION):
	'''Parse input URL into paths tuple for further processing
	
	>>> parse_into_paths('http://test.org/x.py', DESTINATION='TEST') # doctest: +ELLIPSIS
	('x.py', 'http://test.org', 'Documents/TEST', '/private/var/.../TEST', '/priv.../TEST/x.py', True)'''
	
	url_tuple = urlparse.urlparse(input_url)
	scheme, netloc, basename = url_tuple.scheme, url_tuple.netloc, os.path.basename(url_tuple.path)
	input_short = urlparse.urlunparse(iter_pad(len(url_tuple), scheme, netloc, ''))
	output_short = os.path.join(HOME, DESTINATION)
	output_dir = os.path.join(left_subpath_upto(sys.argv[0], HOME), DESTINATION)
	output_path = os.path.join(output_dir, basename)
	is_Python = os.path.splitext(basename)[1].lower() == '.py'
	return basename, input_short, output_short, output_dir, output_path, is_Python
	
def copy_url(input_url):
	'''Write a copy of the file at input_url to HOME/DESTINATION
	if the destination directory doesn't exist, it is created
	if the destination file already exists, the user can cancel or overwrite
	if it is a Python file, a comment line is added to log the origin'''
	
	basename, input_short, output_short, output_dir, output_path, is_Python = parse_into_paths(input_url)
	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
		console.hud_alert('Created destination directory {}'.format(output_short))
	if os.path.exists(output_path):
		try:
			console.alert('Duplicate file',
			'{} already exists in {}'.format(basename, output_short),
			'Overwrite') # or Cancel
		except KeyboardInterrupt:
			return
			
	with contextlib.closing(urllib.urlopen(input_url)) as input:
		data = input.read()
		console.hud_alert('Got {} ({} chars) from {}'.format(basename, len(data), input_short))
	with open(output_path, 'wb') as output:
		if is_Python:
			datetime = time.strftime('%a %d-%b-%Y %H:%M:%S', time.gmtime())
			output.write('# Retrieved from {} on {}\n\n'.format(input_url, datetime))
		output.write(data)
		console.hud_alert('Wrote {} to {}'.format(basename, output_short))
		
def main():
	'''App extension logic, with unit tests if run within Pythonista'''
	
	if appex.is_running_extension():
		if appex.get_url():
			copy_url(appex.get_url())
			appex.finish()
		else:
			console.hud_alert('No input URL found', 'error')
	else:
		console.hud_alert('This script must be run from the sharing extension', 'error')
		import doctest
		doctest.testmod()
		
if __name__ == '__main__':
	main()
