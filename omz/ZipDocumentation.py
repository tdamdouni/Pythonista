# coding: utf-8

# https://forum.omz-software.com/topic/2455/dialogs-module-in-1-6-very-nice-date-and-time-implementation/8

from __future__ import print_function
import os
import zipfile


# copied from stackflow
# http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    documents_path = os.path.expanduser('~/Documents')
    zip_file = os.path.join(documents_path , 'web_help_file_docs.zip')
    documentation_path = os.path.join(os.path.split(os.__file__)[0],
    '''../../../Documentation/''' )
    print('Starting Zip....')
    
    zipf = zipfile.ZipFile(zip_file, 'w')
    zipdir(documentation_path, zipf)
    zipf.close()
    print('Zip completed')