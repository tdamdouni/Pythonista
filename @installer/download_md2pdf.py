# https://gist.github.com/SpotlightKid/9e03a7823827a1841b6b
#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""Download Zip bundle of Python package requirements for MarkdownPDF.py
and extract them to 'site-packages' sub-directory.

This is meant for Pythonista (an iOS app) users as an easy way to install
these packages.

Packages included in the Zip bundle:

* markdown2pdf
* PyPDF2
* Reportlab (without C extensions)
* xhtml2pdf

"""
from __future__ import print_function

import hashlib, os, sys, urllib, zipfile
from os.path import expanduser, isdir, join

ZIPFN = 'markdown2pdf.zip'
ZIPURL = 'http://chrisarndt.de/projects/markdown2pdf/' + ZIPFN
SHA256_DIGEST = "eadfffc65cf13a3333ae809e61fa93f508513a19a49314b62e4adcbecebe6cf0"
SITE_PACKAGES = join(expanduser('~'), 'Documents', 'site-packages')

def print_progress(blocks, bsize, total):
    if blocks and total > 0:
        amount = blocks * bsize
        if amount < total:
            print('\b\b\b\b%3i%%' % (amount / (total / 100.)), end='')

print("Downloading zip archive '%s'...     " % ZIPFN, end='')
urllib.urlretrieve(ZIPURL, ZIPFN, print_progress)
print('\b\b\b\b100%')

with open(ZIPFN, 'rb') as f:
    print("Checking file integrity... ", end='')
    sha256 = hashlib.sha256()
    sha256.update(f.read())
    digest = sha256.hexdigest()
    if not digest == SHA256_DIGEST:
        print("\nSHA-256 checksum mismatch.")
        print("Expected: %s" % SHA256_DIGEST)
        print("Actual: %s" % digest)
        sys.exit(1)
    else:
        print('ok.')

with zipfile.ZipFile(ZIPFN) as z:
    print("Extracting zip file to '~/Documents/site-packages'... ", end='')
    if not isdir(SITE_PACKAGES):
        os.mkdir(SITE_PACKAGES)
    z.extractall(SITE_PACKAGES)

os.unlink(ZIPFN)
print("done.")