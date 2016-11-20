import bs4, importlib, requests  #, pkgutil

modules = '''bottle bs4 cffi ctypes dateutil dropbox ecdsa evernote faker feedparser flask html5lib
             itsdangerous jedi jinja2 markdown markdown2 matplotlib mechanize numpy oauth2 paramiko
             PIL pyflakes pygments pyparsing PyPDF2 pytz qrcode reportlab requests simpy six
             sqlalchemy sympy  werkzeug wsgiref xhtml2pdf xmltodict yaml'''.split()

# Translate from Python module --> PyPI module name
pypi_dict = { 'bs4'      : 'beautifulsoup4',
              'dateutil' : 'py-dateutil',
              'faker'    : 'Faker',
              'yaml'     : 'PyYAML' }

def get_module_version(in_module_name = 'requests'):
	mod = importlib.import_module(in_module_name)
	fmt = "### hasattr({}, '{}')".format(in_module_name, '{}')
	for attr_name in '__version__ version __VERSION__ VERSION'.split():
		if hasattr(mod, attr_name):
			if attr_name != '__version__':
				print(fmt.format(attr_name))
			the_attr = getattr(mod, attr_name)
			if isinstance(the_attr, tuple):  # mechanize workaround
				the_attr = '.'.join([str(i) for i in the_attr[:3]])
			return the_attr() if callable(the_attr) else the_attr
	return '?' * 5
	
def get_module_version_from_pypi(module_name = 'bs4'):
	module_name = pypi_dict.get(module_name, module_name)
	url = 'https://pypi.python.org/pypi/{}'.format(module_name)
	soup = bs4.BeautifulSoup(requests.get(url).content)
	vers_str = soup.title.string.partition(':')[0].split()[-1]
	if vers_str == 'Packages':
		return soup.find('div', class_='section').a.string.split()[-1]
	return vers_str
	
#for pkg in pkgutil.walk_packages():
#    print ('{:<10} {}'.format(pkg[1], get_module_version(pkg[1])))
#print('=' * 16)

fmt = '| {:<10} | {:<7} | {:<7} |'

print('```') # start the output with a markdown literal
print(fmt.format('module', 'local', 'PyPI'))
print(fmt.format('name', 'version', 'version'))
div = fmt.format('-' * 10, '-' * 7, '-' * 7)
print(div)

for module_name in modules:
	local_version = get_module_version(module_name)
	pypi_version  = get_module_version_from_pypi(module_name)
	#if local_version != pypi_version and '?' not in local_version:
	print(fmt.format(module_name, local_version, pypi_version))
print(div)
print('```')  # end of markdown literal

