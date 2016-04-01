"""Compatiblity layer between python 2 and python 3 for some basic stuff

In future will also provide compatiblity for Editorial.app/Pythonista.app for iOS.
"""
from codecs import open

try:
    unicode = unicode
    no_unicode = False
except NameError:
    no_unicode = True
    unicode = str


def _str_(object):
    if no_unicode:
        return object.__unicode__()
    else:
        return unicode(object).encode('utf-8')


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
