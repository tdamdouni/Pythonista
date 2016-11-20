# coding: utf-8
import bs4, importlib, os, platform, plistlib, requests, sys  #, pkgutil

# Translate from Python module --> PyPI module name
pypi_dict = { 'bs4'       : 'beautifulsoup4',
              'dateutil'  : 'py-dateutil',
              'faker'     : 'Faker',
              'sqlite3'   : 'pysqlite',
              'yaml'      : 'PyYAML',
              'xhtml2pdf' : 'pisa',
              'Crypto'    : 'pycrypto',
              'PIL'       : 'Pillow' }

modules = '''bottle bs4 Crypto dateutil dropbox ecdsa evernote faker feedparser
             flask html2text html5lib httplib2 itsdangerous jedi jinja2
             markdown markdown2 matplotlib mpmath numpy oauth2 paramiko
             parsedatetime PIL pycparser pyflakes pygments pyparsing PyPDF2
             pytz qrcode reportlab requests simpy six sqlalchemy sqlite3 sympy
             thrift werkzeug wsgiref xmltodict yaml'''.split()

## Removed: mechanize midiutil screenplain xhtml2pdf

def get_module_version(in_module_name='requests'):
	mod = importlib.import_module(in_module_name)
	fmt = "### hasattr({}, '{}')".format(in_module_name, '{}')
	for attr_name in '__version__ version __VERSION__ PILLOW_VERSION VERSION'.split():
		if in_module_name == 'markdown' and attr_name == '__version__':
			continue
		if in_module_name == 'reportlab':
			attr_name = 'Version'
		if hasattr(mod, attr_name):
			if attr_name != '__version__':
				print(fmt.format(attr_name))
			the_attr = getattr(mod, attr_name)
			#if isinstance(the_attr, tuple):  # mechanize workaround
			#    the_attr = '.'.join([str(i) for i in the_attr[:3]])
			return str(the_attr() if callable(the_attr) else the_attr)
	return '?' * 5
	
def get_module_version_from_pypi(module_name='bs4'):
	module_name = pypi_dict.get(module_name, module_name)
	url = 'https://pypi.python.org/pypi/{}'.format(module_name)
	soup = bs4.BeautifulSoup(requests.get(url).content, 'html5lib')
	vers_str = soup.title.string.partition(':')[0].split()[-1]
	if vers_str == 'Packages':
		return soup.find('div', class_='section').a.string.split()[-1]
	return vers_str
	
'''
for _, pkg_name, _ in pkgutil.walk_packages():
    #print(pkg)
    #pkg_name = pkg[1]
    if 'Gist Commit' in pkg_name:
        sys.exit(pkg_name)
    if '.' in pkg_name:
        continue
    '#''
    if ('ctypes.test.test' in pkg_name
     or 'unittest.__main__' in pkg_name
     or 'numpy.ma.version' in pkg_name
     or 'numpy.testing.print_coercion_tables' in pkg_name
     or 'sympy.mpmath.libmp.exec_py3' in pkg_name
     or 'pycparser._build_tables' in pkg_name
     or 'FileBrowser' in pkg_name):
        continue
    '#''
    #if pkg_name not in ['test_blasdot', 'nose']:
    with open('versions.txt', 'w') as out_file:
        out_file.write(pkg_name)
    #print(pkg_name)
    try:
        mod_vers = str(get_module_version(pkg_name)).strip('?')
        if mod_vers:
            print('{:<10} {}'.format(pkg_name, mod_vers))
    except (ImportError, ValueError) as e:
        print('{:<10} {}'.format(pkg_name, e))
print('=' * 16)
'''

def pythonista_version():
	plist = plistlib.readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
	return '{CFBundleShortVersionString} ({CFBundleVersion})'.format(**plist)
	
print('```') # start the output with a markdown literal
fmt = 'Pythonista version {0} running Python {1} on iOS {2} on an {4}.'
print(fmt.format(pythonista_version(), platform.python_version(), *platform.mac_ver()))
print('=' * 57)

fmt = '| {:<13} | {:<11} | {:<11} | {}'
div = fmt.format('-' * 13, '-' * 11, '-' * 11, '')
print(fmt.format('module', 'local', 'PyPI', ''))
print(fmt.format('name', 'version', 'version', ''))

print(div)
for module_name in modules:
	local_version = get_module_version(module_name)
	pypi_version  = get_module_version_from_pypi(module_name)
	if '?' in local_version or '$' in local_version:
		advise = local_version
	else:
		advise = '' if local_version == pypi_version else 'Upgrade?'
	print(fmt.format(module_name, local_version, pypi_version, advise))
print(div)
print('```')  # end of markdown literal
print('=' * 16)

