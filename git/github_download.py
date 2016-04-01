# https://gist.github.com/SpotlightKid/04c2b5ce5978c0d66e6e
"""Prompt user for URL and filename and download the remote resource to a file.

If the clipboard contains a HTTP(S) or FTP(S) URL, the URL input dialog is
pre-filled with it.

The suggested local filename is extracted from the URL, if possible.

If a github file viewer URL is given, it is transformed into the matching
raw file access URL, which makes it easier to download files on github you
are viewing in your browser. Just copy the URL to the clipboard, change to
Pythonista and run this script.

""" 
import os
import re
import tempfile
import urllib2
import urlparse

from os.path import basename, exists
from urllib import unquote

import console
import editor

CHUNKSIZE = 4096

def download(args):
    if args:
        url = args[0]
    else:
        try:
            import clipboard
            cb = clipboard.get().strip()
            if not re.search('^(ht|f)tps?://', cb):
                cb = ''
            url = console.input_alert('Enter URL', 'Download file from URL:',
                cb, 'Download')
        except KeyboardInterrupt:
            return

    # convert github file viewer URLs into raw file URLs
    urlparts = urlparse.urlparse(url)
    try:
        auth, server = urlparts.netloc.split('@')
    except:
        server = urlparts.netloc

    server = server.split(':')[0]
    if server == 'github.com' and '/blob' in urlparts.path:
        urlparts = list(urlparts)
        urlparts[1] = urlparts[1].replace('github.com', 'raw.githubusercontent.com')
        urlparts[2] = urlparts[2].replace('/blob', '')
        url = urlparse.urlunparse(urlparts)

    try:
        r = urllib2.urlopen(url)
    except urllib2.URLError as exc:
        print(exc)
        console.hud_alert("Download error (see console)", 'error')
        return

    content_type = r.info().get('content-type')
    urlparts = urlparse.urlparse(r.geturl())
    fn = basename(unquote(urlparts.path))

    while True:
        try:
            fn = console.input_alert('Enter filename', "Save download as:", fn)
            if exists(fn):
                choice = console.alert('Overwrite file?',
                    'File exists. Enter new filename, overwrite or cancel?',
                    'New filename', 'Overwrite')
                if choice == 2:
                    break
            else:
                break
        except KeyboardInterrupt:
            return

    try:
        # trigger error early in case there are permission problems 
        if not exists(fn):
            open(fn, 'wb').close()

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            while True:
                chunk = r.read(CHUNKSIZE)
                if not chunk:
                    break
                temp.write(chunk)
    except Exception as exc:
        print(exc)
        console.hud_alert("Download error (see console)", 'error')
        try:
            os.unlink(temp.name)
        except:
            pass
        return        
    else:
        os.rename(temp.name, fn)
    
    if content_type.startswith('text/'):
        editor.open_file(fn)

if __name__ == '__main__':
    import sys
    download(sys.argv[1:])