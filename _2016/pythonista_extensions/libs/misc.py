# coding: utf-8

# https://gitlab.com/atronah/pythonista_extensions/tree/master

import os
import logging
import appex
from urllib.parse import urlparse
from urllib.request import urlopen
import contextlib

def coroutine(func):
    def wrapped(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return wrapped


def add_attr(**named_attributes):
    def decorator(func):
        for key, value in named_attributes.items():
            setattr(func, key, value)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapped
    return decorator
    
    
@coroutine
def writer(*args, **kwargs):
    '''Creates coroutine (async function) to write received data into cpecified file.
    All arguments passes into built-in open() function
    '''
    total_len = 0
    filename = ''
    with open(*args, **kwargs) as f:
        filename = f.name
        data = (yield 0)
        while data:
            total_len += len(data)
            f.write(data)
            data = (yield total_len)
            
            
def get_sources():
    '''
    >>> [source for source, type in get_sources() if type == 'path'][0].endswith('/misc.py')
    True
    '''
    type_getters = []
    if appex.is_running_extension():
        type_getters.append(('path', appex.get_file_paths))
        type_getters.append(('url', appex.get_urls))
        type_getters.append(('text', appex.get_text))
    else:
        import editor
        type_getters.append(('path', editor.get_path))
        type_getters.append(('text', editor.get_text))
        
    for type, func in type_getters:
       sources = func()
       if not isinstance(sources, (list, tuple)):
           sources = [sources]
       for source in sources:
           yield source, type
           

def get_source_content(source, type='text'):
    '''Retrieves content from source accordance with its type.
    Supported types:
        - text
        - url
        - path
        
    >>> get_source_content('test', 'text')
    b'test'
    
    >>> get_source_content('/test/file', 'path')
    
    >>> import sys
    >>> b'def get_source_content(' in get_source_content(sys.argv[0], 'path')
    True
    
    >>> import sys
    >>> b'def get_source_content(' in get_source_content('file://' + sys.argv[0], 'url')
    True
    '''
    assert type in ('text', 'url', 'path')

    if type == 'text':
        return source.encode('utf8')
    elif type == 'url':
        schema = urlparse(source)[0]
        if schema == 'https':
            logging.error('URL Schema "{}" doesn''t support'.format(schema))
            return None
        try:    
            with contextlib.closing(urlopen(source)) as input:
                return input.read()
        except Exception as e:
            logging.error('Error\n"{}"\nfor URL\n"{}"'.format(e, source))
    elif type == 'path':
        if os.path.isfile(source):
            with open(source, 'rb') as input:
                return input.read()
        else:
            logging.error('"{}"\nis not file or doesn''t exists'.format(source))
    return None
    
    
if __name__ == '__main__':
    import doctest
    from log import clear_handlers
    clear_handlers()
    logging.getLogger().setLevel(logging.INFO)
    doctest.testmod()
