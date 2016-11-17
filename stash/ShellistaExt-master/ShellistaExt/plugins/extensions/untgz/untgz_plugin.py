import sys
import tarfile

from ... tools.toolbox import bash

def main(self, line):
    do_untgz(line)

shellista = sys.modules['__main__']

def do_untgz(line):
    """Untar/gz a file"""
    files = bash(line)
    if len(files):
        for file in files:
            try:
                with tarfile.open(file, 'r:gz') as tf:
                    tf.extractall('.')
            except IOError as e:
                print 'File: {0} {1}'.format(file, e)

