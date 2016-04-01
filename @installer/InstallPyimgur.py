# coding: utf-8

# https://forum.omz-software.com/topic/2430/how-do-you-upload-images-to-a-forum-discussion/2

import shutil, urllib2, os, zipfile
f=urllib2.urlopen('https://codeload.github.com/Damgaard/PyImgur/zip/master')
with open(os.path.expanduser('~/Documents/pyimgur.zip'),'w') as z:
    z.write(f.read())
z=zipfile.ZipFile(os.path.expanduser('~/Documents/pyimgur.zip'))
z.extractall()
os.remove(os.path.expanduser('~/Documents/pyimgur.zip'))
shutil.copytree(os.path.expanduser('~/Documents/PyImgur-master/pyimgur'), os.path.expanduser('~/Documents/site-packages/pyimgur'))
shutil.rmtree(os.path.expanduser('~/Documents/PyImgur-master'))