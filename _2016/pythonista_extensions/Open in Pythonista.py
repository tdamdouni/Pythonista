# coding: utf-8

# https://gitlab.com/atronah/pythonista_extensions/tree/master

'''
Based on the script GetFromURL (Olaf, Dec 2015, Pythonista 1.6 beta)
See the discussion:
https://forum.omz-software.com/topic/2494/appex-getfromurl-to-share-from-other-apps-to-pythonista
'''

import appex
import console
import os
import sys
from urllib.parse import urlparse, urlunparse
from urllib.request import urlopen
import shutil
import logging
import contextlib
import collections
from libs.log import setup_alert_logging
from libs.misc import writer, add_attr, get_sources, get_source_content


def split_path(path, sentinel):
    '''Left part (subpath) of path upto and including sentinel

    >>> print(split_path('a/b/c', 'b'))
    ('a/b', 'c')
    
    >>> print(split_path('/', 'test'))
    ('/', '')
    '''

    left = path
    right = ''
    while left:
        path, tail = os.path.split(left)
        if tail == sentinel:
            break
        right = os.path.join(tail, right) if right else tail
        left = path if path != left else ''        
    if left == '':
        left = os.path.join(path, right)
        right = ''
    return left, right


def get_destination_path(source):
    ''' Calcualate destination path based on source path or url
    
    >>> get_destination_path('/var/test/File Provider Storage/dir/subdir/file') # doctest: +ELLIPSIS
    ('/private/var/.../Documents/dir/subdir/file', 'dir/subdir/file')
    '''
    schema, netloc, path = urlparse(source)[:3]
    if not schema or schema == 'file':
        short_path = split_path(source, 'File Provider Storage')[1]
    else:
        short_path = netloc + path
        if (schema == 'http' and 
            os.path.splitext(short_path)[1].lower() != '.html'):
            short_path += '.html'

    if not short_path:
        short_path = 'Untitled.txt'
    
    try:
        short_path = console.input_alert('Confirmation', 
                                         'Before opening save as ...', 
                                         short_path, 
                                         'Confirm')
    except KeyboardInterrupt:
        short_path = ''
    
    full_path = os.path.join(split_path(sys.argv[0], 'Documents')[0], short_path)
    
    return full_path, short_path
    
    
def file_overwrite_confirm(filepath, yes_to_all_button=False):
    '''Shows file overwrite confirmation dialog
    '''
    buttons = ['Yes', 'No']
    if yes_to_all_button:
        buttons.insert(1, 'Yes to all')
    user_choise = console.alert('Confirmation', 
                                '"{}"\nalready exists,\n'
                                'overwrite?'.format(filepath),
                                *buttons,
                                hide_cancel_button=True)
    return user_choise % len(buttons)
    

@add_attr(overwrite=False)
def copy(src, dst, overwrite=False, dst_root=None):
    '''Recursively copies src into dst with overwrite promt dialog if dst exists.
    If overwrite=True, all existed files will be overwrited silently, 
    otherwise promt dialog will be displayed.
    dst_root used to calculate relative short path for destination file to show in prompt dialogs.
    '''
    copy.overwrite = overwrite
    if not dst_root:
        dst_root = dst
    result = True
    if os.path.isdir(src):        
        logging.debug('looking {}'.format(src))
        for name in os.listdir(src):
            if name.startswith('.'): 
                continue
            sub_src = os.path.join(src, name)
            if not copy(sub_src, 
                        os.path.join(dst, name) + 
                               (os.sep if os.path.isdir(sub_src) else ''),
                        copy.overwrite,
                        dst_root):
                return False
    elif os.path.isfile(src):
        dst_dir = os.path.dirname(dst)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        dst_path = os.path.join(dst_dir, os.path.basename(src))
        rel_path = os.path.relpath(dst_path, dst_root)
        if not copy.overwrite and os.path.exists(dst_path):
            is_confirm = file_overwrite_confirm(rel_path, True)
            if not is_confirm:
                return False
            elif is_confirm == 2: # yes to all
                copy.overwrite = True
        logging.debug('copying {} -> {}'.format(src, dst))
        copy_result = shutil.copy2(src, dst)
        if not os.path.exists(copy_result):
            logging.error('Copying result doesn''t exists ({})'.format(copy_result))
            return False
    else:
        logging.error('unkwonw type of source: {}'.format(src))
        return False
    return result
    

def process(source, type='text'):
    '''Process source in accordance with its type
    Supported types:
    - text - get data from source and put it into single file in Pythonista
    - path - copy file system object (single file or directory with files) from source to Pythonista
    - url - get data from source URL and put it into single file in Pythonista
    returns False if source is empty and True otherwise
    '''
    assert type in ('text', 'url', 'path')

    if not source:
        return False
    
    if source == os.sep:
        if console.alert('Confirmation', 
                         'Do you really want to open "{}" in Pythonista'.format(source),
                         'Yes', 'No',
                         hide_cancel_button=True) == 2:
             return True
    if type == 'url':
        schema = urlparse(source)[0]
        if schema == 'https':
            logging.error('URL Schema "{}" doesn''t support'.format(schema))
            return True
    full_dst, short_dst = get_destination_path(None if type == 'text' else source)
    if not short_dst:
        logging.info('Empty destination')
        return True
    
    overwrite = False
    if os.path.exists(full_dst):
        is_many_files = type == 'path' and os.path.isdir(full_dst)
        overwrite_state = file_overwrite_confirm(short_dst, 
                                                 is_many_files)
        if not overwrite_state:
            return True
        elif overwrite_state == 2: # Yes to all
            overwrite = True
    elif not os.path.exists(os.path.dirname(full_dst)):
        os.makedirs(os.path.dirname(full_dst))
    
    result_message = 'Successful.\nLook in\n{}'.format(short_dst)
    if type == 'path':
        if not copy(source, full_dst, overwrite):
            return True
    else:
        output = writer(full_dst, 'wb')
        content = get_source_content(source, type)
        total_len = len(content)
        output.send(content)
        if type == 'url':
            result_message = 'Got {} chars\nfrom {}\ninto{}'
            result_message = result_message.format(total_len, source, short_dst)
    logging.info(result_message)
    return True
           

def main():
    setup_alert_logging()

    for source, type in get_sources():
        if process(source, type):
            return True
  
 
if __name__ == '__main__':
    main()
