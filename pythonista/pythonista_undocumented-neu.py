# coding: utf-8
import bs4, importlib, inspect, requests, itertools

modules = '''canvas clipboard console contacts editor keychain linguistictagger
             location motion notification photos scene sound speech ui'''.split()
modules += '''appex cb ctypes dialogs sk'''.split()  # modules added in Pythonista v1.6 Beta

def inspect_functions(module_name):
	module = importlib.import_module(module_name)
	return [member[0] for member in inspect.getmembers(module)
	if callable(member[1]) and not member[0].startswith('__')]
	
def inspect_attributes(module_name):
	module = importlib.import_module(module_name)
	return [member[0] for member in inspect.getmembers(module)
	if not callable(member[1]) and not member[0].startswith('__')]
	
def get_html(module_name):
	fmt = 'http://omz-software.com/pythonista/docs/ios/{}.html'
	return requests.get(fmt.format(module_name)).text
	#import os
   # with open(os.path.join(os.path.split(os.__file__)[0],'../Documentation/ios/{}.html'.format(module_name))) as f:
   #    return f.read()

def website_functions(module_name):
	headerlinks = bs4.BeautifulSoup(get_html(module_name)).find_all('a', 'headerlink')
	return sorted(list(set([hl['href'].partition('.')[2]
	for hl in headerlinks if '.' in hl['href']])))
	
def find_module_class_members(module_name):
	'''find all class members in the module'''
	module = importlib.import_module(module_name)
	class_members= [find_class_members(cls)
	for cls in [m for m in inspect.getmembers(module)
	if isinstance(m[1],type)] if not isbuiltin(cls[1])]
	return set(itertools.chain(*class_members)) # unique and flatten()
	
def find_class_members(cls):
	'''find all members of class tuple (classname,class). '''
	return [m for m in [find_oldest_ancestor(member[0],cls[1]) for member in inspect.getmembers(cls[1]) if not member[0].startswith('__')] if m]
	
def find_oldest_ancestor(member_name,thiscls):
	'''given a member name, return string of form ancestor.member_name where an estor is the oldest ancestor containing that attribute, or return None for ancestor == a builtin'''
	for cls in [c for c in thiscls.mro()[-2::-1]]:
		if hasattr(cls, member_name):
			return '.'.join((cls.__name__,member_name)) if not isbuiltin(cls) else None
def isbuiltin(cls):
	return cls.__module__=='__builtin__'
def undocumented_functions(module_name):
	print('looking for undocumented in {} module...'.format(module_name))
	inspect_funcs = inspect_functions(module_name)
	inspect_attr = inspect_attributes(module_name)
	class_members = find_module_class_members(module_name)
	website_funcs = website_functions(module_name)
	
	return sorted(itertools.chain(['{}.{}()'.format(module_name, f)
	for f in inspect_funcs if f not in website_funcs],
	['{}.{}'.format(module_name, f)
	for f in inspect_attr if f not in website_funcs],
	['{}.{}'.format(module_name,f) for f in class_members if f not in website_funcs]))
	
undocumented = [x for x in [undocumented_functions(module_name)
                                for module_name in sorted(modules)]]
print('=' * 40)
print('\n'.join(itertools.chain(*undocumented)))  # flatten()

