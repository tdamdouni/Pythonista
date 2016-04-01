# coding: utf-8

# @Phuket2

# https://forum.omz-software.com/topic/2447/hackathon-challenge-set-by-ccc-started-new-thread/8

# https://github.com/Phuket2/Pythonista/blob/master/Hackathons/create_stub_files.py

'''
Hackathon Challange: write code that uses the Python inspect module to find all the functions and methods in the ui module and auto generate a ui.py file that has those same functions and modules stubbed out (with pass statement) such that an editor like sublime or PyCharm on Windoze or a real computer (e.g. Mac) will do autocompletion on all functions and methods of Pythonista ui code. All winning entries must 1) deliver correct code completion for all ui methods and functions, 2) pass all PyCharm PEP8 compliance tests (esp. line length) and 3) be posted in a GitHub repo by 8am Eastern time on Monday 14 Dec 2015 time. If there are multiple entries that pass the above tests then the shortest number of (nonblank) lines of code wins.

Can you complete the challenge?!?
'''

'''
	PEP8 
	Limit all lines to a maximum of 79 characters.
'''

import inspect

_module_alias = {'canvas' :'ui',
						}

def PEP8_split_line(l):
	# assuming its a class or function statement
	
	part = l.partition('(')
	# try the nice way first
	l2 = part[0] + part[1] + '\n' + '\t\t' + part[2]
	
	# if the params exceed the line length, then we just
	# go coyote ugly!!
	if part[2] > 79:
		params = part[2].split(',')
		l2 = part[0] + part[1] + ',\t\n'.join(p for p in params)
			
	return l2
	
def get_code_block_stubs(code):
	'''
		Source code of a class, function, property
		return a list of lines aka code_lines to write out
		to a a file or the console.
	'''
	
	the_code = code[0].splitlines()
	code_lines = []
	
	'''
		create a list of dicts of code lines
		we care about. class, def
		
		i didnt realise unil i seen the posting that putting 
		pass : on the same line was acceptable.
		My lack of knowedgle.
		
		Thats ok, i will leave mine like this.
		I can see i am doing a lot of extra proccessing.
		I think could have done all the work in the list comp.
		
		Maybe it more flexible like this. Even though thats 
		not the goal :(
		
	'''
	
	wanted_lines = [ {	'line_no' : ln,
							 	'token': l.strip('\t ').rsplit(' ')[0], 
								'delim' : '\t' if l[0].isalpha() else l[0],
								'delim_len' : len(l) - len(l.lstrip(l[0])),
								'the_line' : l.lstrip('\t ')
							}
		for ln, l in enumerate(the_code) if l and
			l.strip('\t ').rsplit(' ')[0] == 'class' or
			l.strip('\t ').rsplit(' ')[0] == 'def'
			]
			
	
	indent = 0
	indent_adjust = 0 
	
	for ln, d in enumerate(wanted_lines):
		if len(d['the_line']) > 75:
			#raise Exception('line length exceeds PEP8 79 chars')
			
			d['the_line'] = PEP8_split_line(d['the_line'])
		
		if ln:
			if d['delim_len'] == ll['delim_len']:
				indent_adjust = 0
			elif d['delim_len'] > ll['delim_len']:
				indent_adjust = 1
			elif d['delim_len'] < ll['delim_len']:
				indent_adjust = -1
		
		# edge case @omz 		
		if ln:
			if ll['token'] == 'class':
				indent_adjust = 1
			
		indent += indent_adjust
			
		code_lines.append('{}{}'.format('\t' * indent, (d['the_line'])))
		if not d['token'] == 'class':
			code_lines.append('{}pass\n'.format('\t' * (indent+1)))
			
		# ll is the last dict
		ll = d

			
	return code_lines
	

'''
	i had done the filtering in the list comp,
	serveral different ways. but just to ugly even though
	trying to get the least code lines.
	i still prefer to do this. 
	Actually depending on how you count lines about the same number
	 
	Also easy to fine tune the filter here
'''	
def _inspect_predicate(obj):
	if inspect.isclass(obj) and '<class' in str(obj):
		return True
	
	if inspect.isfunction(obj) and '<function' in str(obj):
		return True
	
	return False
	
def _predicate_module_vars(obj):
	if not inspect.ismethoddescriptor(obj):
		return True
		
	return False	

	
def process_module(in_module):
	
	module = in_module
	mod_str = str(module.__name__)
	
	'''
		look at a dict to see if we are using something diff
		than the module name prefix for the module 
		level vars...
		canvas for example
	'''
	for k , v in _module_alias.iteritems():
		if k == str(module.__name__):
			mod_str = str(v)
			break		
	
	# a list of the classes and functions we are intrested in
	# _inspect_predicate, handles the filtering...
	_list = [ (name, obj) for name,obj in 
		inspect.getmembers(module, _inspect_predicate)
	]
	
	_list_mod_vars = [ '{}.{}'.format(mod_str, name)
			for name,obj in inspect.getmembers(module , _predicate_module_vars)
			if name.isupper()
	]
	
	
	with open('{}_{}.py'.format(module.__name__, 'stub') , 'a') as f:
		f.truncate(0)
		
		'''
			Write out the module level vars...
			i am guessing i went a little wrong here in identifying
			what a module var is. i am not sure...
		'''
		bytecount = 0
		for var in _list_mod_vars:
			if len(var) + bytecount < 76:
				f.write(var + ' ,')
				bytecount += len(var)
			else:
				f.write('\n' + var + ',')
				bytecount = len(var)
		f.write('\n\n')

		# iterate over each of the objects of interest.
		for elms in _list:
			
			# retrive the source code for the object
			# decided not use source lines
			f_code =  str(inspect.getsource(elms[1])), '\n'
			
			# write each line out to the file...
			for l in  get_code_block_stubs(f_code):
				#print l
				f.write(l + '\n')

if __name__ == '__main__':
	# cb fails, with the module level vars for some reason?
	module_list = ['ui', 'dialogs', 'appex', 'notification',
							'canvas', 'clipboard']
	module_list = ['ui']
	for mod in module_list:
		_mod = __import__(mod)
		process_module(_mod)
	