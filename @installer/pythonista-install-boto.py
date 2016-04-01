# Source: https://gist.github.com/najibninaba/5062153
# 
# This script installs Boto in Pythonista. Run this script in your root folder and it will download and install Boto along with its
# dependencies. To use Boto, be sure to add boto-module in your sys.path before importing boto like so:
# import sys; sys.path.append('boto-module')
# import boto.ec2
#
# Credits:
# This script is inspired by omz's Evernote Installer script: https://gist.github.com/omz/5048588
#


packages = ['https://pypi.python.org/packages/source/b/boto/boto-2.8.0.tar.gz',
    'https://pypi.python.org/packages/source/m/mock/mock-1.0.1.tar.gz',
    'https://pypi.python.org/packages/source/r/rsa/rsa-3.1.1.tar.gz',
    'https://pypi.python.org/packages/source/t/tox/tox-1.4.zip',
    'https://pypi.python.org/packages/source/S/Sphinx/Sphinx-1.1.3.tar.gz',
    'https://pypi.python.org/packages/source/s/simplejson/simplejson-2.5.2.tar.gz',
    'http://argparse.googlecode.com/files/argparse-1.2.1.tar.gz',
    'https://pypi.python.org/packages/source/u/unittest2/unittest2-0.5.1.tar.gz'
]

configparser_src = 'http://hg.python.org/cpython/raw-file/70274d53c1dd/Lib/ConfigParser.py'

import shutil
import urllib
from urlparse import urlparse
import tarfile
import zipfile
import os


def create_module_dir():
    try:
        os.mkdir('boto-module')
    except:
        pass


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.path.rpartition('/')[-1]

def is_zipfile(f):
    return f.endswith('.zip')

def is_targzfile(f):
    return f.endswith('.tar.gz')

def download_packages():
    for f in packages:
        print('Downloading %s' % f)
        filepath, headers = urllib.urlretrieve(f)
        print('Extracting %s' % filepath)
        filename = get_filename_from_url(f)
        if is_targzfile(filename):
            t = tarfile.open(filepath, 'r')
            t.extractall()
            t.close()
        elif is_zipfile(filename):
            z = zipfile.ZipFile(filepath, 'r')
            z.extractall()
            z.close()

def install_configparser_src():
    print('Installing ConfigParser...')
    filepath, headers = urllib.urlretrieve(configparser_src)
    shutil.move(filepath, 'boto-module/ConfigParser.py')

def install_packages():
    print('Installing boto...')
    shutil.move('boto-2.8.0/boto', 'boto-module/boto')
    shutil.rmtree('boto-2.8.0')

    print('Installing mock...')
    shutil.move('mock-1.0.1/mock.py', 'boto-module/mock.py')
    shutil.rmtree('mock-1.0.1')

    print('Installing rsa...')
    shutil.move('rsa-3.1.1/rsa', 'boto-module/rsa')
    shutil.rmtree('rsa-3.1.1')

    print('Installing tox...')
    shutil.move('tox-1.4/tox', 'boto-module/tox')
    shutil.rmtree('tox-1.4')

    print('Installing Sphinx...')
    shutil.move('Sphinx-1.1.3/sphinx', 'boto-module/sphinx')
    shutil.rmtree('Sphinx-1.1.3')

    print('Installing simplejson...')
    shutil.move('simplejson-2.5.2/simplejson', 'boto-module/simplejson')
    shutil.rmtree('simplejson-2.5.2')

    print('Installing argparse...')
    shutil.move('argparse-1.2.1/argparse.py', 'boto-module/argparse.py')
    shutil.rmtree('argparse-1.2.1')

    print('Installing unittest2...')
    shutil.move('unittest2-0.5.1/unittest2', 'boto-module/unittest2')
    shutil.rmtree('unittest2-0.5.1')

def reload_pythonista_editor():
    print('Reloading Pythonista editor')
    import editor
    editor.reload_files()


if __name__ == '__main__':
    create_module_dir()
    download_packages()
    install_packages()
    install_configparser_src()
    reload_pythonista_editor()
    print('All done!')
    


