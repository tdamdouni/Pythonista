# https://gist.github.com/omz/4076111

# install missing xmlrpclib module
import requests
r = requests.get('http://hg.python.org/cpython/raw-file/7db2a27c07be/Lib/xmlrpclib.py')
with open('xmlrpclib.py', 'w') as f:
	f.write(r.text)