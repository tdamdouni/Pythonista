# https://gist.github.com/671620616/3e04758185af8f98bf72
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 08 15:29:00 2015

Prompt for a GitHub user name, the name of a repo, and download it.
Please note: this is *NOT* a cloning tool! It simply downloads the files in the repo.

"""

import os
import urllib
import zipfile
import random

print "Getting URL..."
url_format = 'https://www.github.com/{user}/{repo}/archive/master.zip'
user = raw_input('Please enter the name of the user > ')
repo = raw_input('Please enter the name of the repo > ')

print "Preparing..."
url = url_format.format(user=user, repo=repo)
downloadname = str(random.randint(0x000000, 0xFFFFFF)) + "_master.zip"

print "Downloading..."
urllib.urlretrieve(url, downloadname)

print "Extracting..."
zipped = zipfile.ZipFile(downloadname, 'r')
zipped.extractall()
zipped.close()

print "Cleaning up..."
os.remove(downloadname)