import os, os.path, sys, urllib2, requests

class PyPiError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def _chunk_report(bytes_so_far, chunk_size, total_size):
    if (total_size != None):
        percent = float(bytes_so_far) / total_size
        percent = round(percent*100, 2)
        print 'Downloaded %d of %d bytes (%0.2f%%)' % (bytes_so_far, total_size, percent)
        if bytes_so_far >= total_size:
            print ''
    else:
        print 'Downloaded %d bytes' % (bytes_so_far)

def _chunk_read(response, chunk_size=32768, report_hook=None, filename=None):
    file_data = []
    if response.info().has_key('Content-Length'):
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
    else:
        # No size
        total_size = None
        if report_hook:
            print '* Warning: No total file size available.'
    if (filename == None) and (response.info().has_key('Content-Disposition')):
        # If the response has Content-Disposition, we take file name from it
        try:
            filename = response.info()['Content-Disposition'].split('filename=')[1]
            if filename[0] == '"' or filename[0] == "'":
                filename = filename[1:-1]
        except Exception:
            sys.exc_clear()
            filename = 'output'
    if (filename == None):
        if report_hook:
            print "* No detected filename, using 'output'"
        filename = 'output'
    bytes_so_far = 0
    while True:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)
        if not chunk:
            break
        else:
            file_data.append(chunk)
        report_hook(bytes_so_far, chunk_size, total_size)
    return (file_data, filename)

def _download(src_dict, print_progress=True):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6;en-US; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9'}
    if print_progress:
        print '* Downloading:', src_dict['url']
    req = urllib2.Request(src_dict['url'], headers=headers)
    response = urllib2.urlopen(req)
    output = src_dict['url'].split('/')[-1].split('#')[0].split('?')[0]
    if print_progress:
        data,filename = _chunk_read(response, report_hook=_chunk_report, filename=output)
    else:
        data,filename = _chunk_read(response, report_hook=None, filename=output)
    if (len(data) > 0):
        try:
            f = open(filename, 'wb')
            for x in data:
                f.write(x)
            f.close()
            if print_progress:
                print '* Saved to:', filename
        except Exception:
            if print_progress:
                print '! Error:', sys.exc_info()[1]
            raise
    else:
        if print_progress:
            print '* Error: 0 bytes downloaded, not saved'

def pypi_download(pkg_name, pkg_ver='', print_progress=True):
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    hits = pypi.package_releases(pkg_name, True)
    if not hits:
        raise PyPiError('No package found with that name')
    if not pkg_ver:
        pkg_ver = hits[0]
    elif not pkg_ver in hits:
        raise PyPiError('That package version is not available')
    hits = pypi.release_urls(pkg_name, pkg_ver)
    if not hits:
        raise PyPiError('No public download links for that version')
    source = ([x for x in hits if x['packagetype'] == 'sdist'][:1] + [None])[0]
    if not source:
        raise PyPiError('No source-only download links for that version')
    return _download(source, print_progress)

def pypi_versions(pkg_name, limit=10, show_hidden=True):
    if not pkg_name:
        return []
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    hits = pypi.package_releases(pkg_name, show_hidden)
    if not hits:
        return []
    if len(hits) > limit:
        hits = hits[:limit]
    return hits

def pypi_search(search_str, limit=5):
    if not search_str:
        return []
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    hits = pypi.search({'name': search_str}, 'and')
    if not hits:
        return []
    hits = sorted(hits, key=lambda pkg: pkg['_pypi_ordering'], reverse=True)
    if len(hits) > limit:
        hits = hits[:limit]
    return hits

def install_xmlrpclib(path='.'):
    # Grab the 2.7.3 version of xmlrpclib - even though Pythonista 1.2 is 2.7.0
    r = requests.get('http://hg.python.org/cpython/raw-file/70274d53c1dd/Lib/xmlrpclib.py')
    lib_file = os.path.join(path, 'xmlrpclib.py')
    with open(lib_file, 'w') as f:
        f.write(r.text)

# The following code is intentionally executed on import of the pipista module.
# It patches the standard import search paths to include the directory pipista
# installs downloaded modules in.
# If you really don't like this functionality, just edit this script to:
# _auto_path = False

_auto_path = True

# Begin library prep

if _auto_path:
    # Get pipista location
    mod_path = os.path.abspath(__file__)
    mod_dir  = os.path.dirname(mod_path)
    lib_dir  = os.path.join(mod_dir, 'pypi-modules')
    if not os.path.exists(lib_dir):
        try:
            os.mkdir(lib_dir)
        except Exception:
            # Fail silently, if we can't make the directory
            sys.exc_clear()
    # Make sure lib_dir exists before adding it to the paths
    if os.path.exists(lib_dir):
        if lib_dir not in sys.path:
            sys.path += [lib_dir]
    # Attempt to load xmlrpclib - not present in Pythonista 1.2
    try:
        import xmlrpclib
    except ImportError:
        # Doesn't seem to be available - attempt to download it.
        sys.exc_clear()
        install_xmlrpclib(lib_dir)
        import xmlrpclib
