#pipista is required to run
import pipista
pipista.pypi_download('Django', '1.6.5')

from urllib import urlretrieve
import tarfile
import shutil
import os
 
print 'Installing django...'
with tarfile.open('Django-1.6.5.tar.gz', 'r') as i:
	i.extractall()
 
shutil.move('Django-1.6.5/django', '.')
shutil.rmtree('Django-1.6.5')
os.remove('Django-1.6.5.tar.gz')
print 'Installation complete.' 
print 'Testing...'
 
import django
print django.VERSION
