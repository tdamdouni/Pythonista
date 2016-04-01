#import nose
import bs4, importlib, requests, pkgutil

# Translate from Python module --> PyPI module name
pypi_dict = { 'bs4'      : 'beautifulsoup4',
              'dateutil' : 'py-dateutil',
              'faker'    : 'Faker',
              'yaml'     : 'PyYAML',
              'Crypto'   : 'pycrypto'}

modules = '''bottle bs4 cffi Crypto ctypes dateutil dropbox ecdsa evernote faker feedparser flask
             html2text html5lib httplib2 itsdangerous jedi jinja2 markdown markdown2 matplotlib
             mechanize mpmath numpy oauth2 paramiko parsedatetime PIL pycparser pyflakes pygments
             pyparsing PyPDF2 pytz qrcode reportlab requests simpy six sqlalchemy sympy thrift
             werkzeug wsgiref xhtml2pdf xmltodict yaml'''
             
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

lsd()
'''

fmt = '| {:<13} | {:<8} | {:<10} |'
div = fmt.format('-' * 13, '-' * 8, '-' * 10)

print('```') # start the output with a markdown literal
print(fmt.format('module', 'local', 'PyPI'))
print(fmt.format('name', 'version', 'version'))

print(div)
for module_name in modules.split():
    local_version = get_module_version(module_name)
    pypi_version  = get_module_version_from_pypi(module_name)
    #if local_version != pypi_version and '?' not in local_version:
    print(fmt.format(module_name, local_version, pypi_version))
print(div)
print('```')  # end of markdown literal
print('=' * 16)

'''
bottle     0.12.5  v.s. 0.12.8  OLDER VERSION
bs4        4.3.2   v.s. 4.3.2   current version
dateutil   1.5-mpl v.s. 2.2     correct version for Python2
dropbox    ?????   v.s. 2.2.0   unclear
ecdsa      0.11    v.s. 0.11    current version
evernote   ?????   v.s. 1.25.0  unclear
faker      ?????   v.s. 0.0.4   unclear
feedparser 5.1.3   v.s. 5.1.3   current version
flask      0.10.1  v.s. 0.10.1  current version
html5lib   0.999   v.s. 0.999   current version
### hasattr(markdown, 'version')
markdown   2.2.0   v.s. 2.5.2   OLDER VERSION
markdown2  2.2.1   v.s. 2.3.0   OLDER VERSION
mechanize  (0, 2, 5, None, None) v.s. 0.2.5  current version
paramiko   1.13.0  v.s. 1.15.2  OLDER VERSION
PIL        ?????   v.s. 1.1.6   unclear
pygments   1.6     v.s. 2.0.1   OLDER VERSION
pyparsing  2.0.1   v.s. 2.0.3   OLDER VERSION
requests   2.2.1   v.s. 2.5.1   OLDER VERSION
six        1.6.1   v.s. 1.9.0   OLDER VERSION
wsgiref    ?????   v.s. 0.1.2   unclear
xmltodict  0.8.7   v.s. 0.9.0   OLDER VERSION
==================================
| module     | local   | PyPI    |
| name       | version | version |
| ---------- | ------- | ------- |
| bottle     | 0.12.5  | 0.12.8  |
| bs4        | 4.3.2   | 4.3.2   |
| dateutil   | 1.5-mpl | 2.2     |
| dropbox    | ?????   | 2.2.0   |
| ecdsa      | 0.11    | 0.11    |
| evernote   | ?????   | 1.25.0  |
| faker      | ?????   | 0.0.4   |
| feedparser | 5.1.3   | 5.1.3   |
| flask      | 0.10.1  | 0.10.1  |
| html5lib   | 0.999   | 0.999   |
### hasattr(markdown, 'version')
| markdown   | 2.2.0   | 2.5.2   |
| markdown2  | 2.2.1   | 2.3.0   |
| mechanize  | 0.2.5   | 0.2.5   |
| paramiko   | 1.13.0  | 1.15.2  |
| PIL        | ?????   | 1.1.6   |
| pyflakes   | 0.7.3   | 0.8.1   |
| pygments   | 1.6     | 2.0.2   |
| pyparsing  | 2.0.1   | 2.0.3   |
| requests   | 2.2.1   | 2.5.1   |
| six        | 1.6.1   | 1.9.0   |
| werkzeug   | 0.9.4   | 0.9.6   |
| wsgiref    | ?????   | 0.1.2   |
| xmltodict  | 0.8.7   | 0.9.1   |
| ---------- | ------- | ------- |
'''
