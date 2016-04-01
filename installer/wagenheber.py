#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# wagenheber.py
#
"""Simple PyPI package installation client for Pythonista.

Currently only supports installing pure Python packages for which a
distribution archive in bdist_wheel format is available on PyPI.

Also doesn't handle dependencies in any way yet.

"""

from __future__ import print_function

import re
import os
import sys
import urllib2
import tempfile
import xmlrpclib

from operator import itemgetter


__version__ = '0.1a'

PYPI_URL = 'http://pypi.python.org/pypi'
PY_VERSION = "%i.%i" % sys.version_info[:2]
PY_VERSION_NODOT = "%i%i" % sys.version_info[:2]
PY_MAJOR_VERSION = str(sys.version_info[0])
ALLOWED_PY_VER = (
    'cp%s' % PY_VERSION_NODOT, 
    'py%s' % PY_VERSION_NODOT,
    'cp%s' % PY_MAJOR_VERSION,
    'py%s' % PY_MAJOR_VERSION,
    PY_MAJOR_VERSION,
    'any'
)
WHEEL_TAGS_RX = re.compile(r"""
    (?P<package>\w*?)
    -(?P<version>.*?)
    (-(?P<build>.*?))?
    -(?P<pyver>[\.\w]*?)
    -(?P<abi>[\.\w]*?)
    -(?P<platform>[\.\w]*?).whl""",
    re.VERBOSE | re.I)


class PyPiError(Exception):
    pass

def _check_py_ver(pkg, versions):
    m = WHEEL_TAGS_RX.match(pkg['filename'])

    if m:
        tags = m.groupdict()
    else:
        tags = {}

    pkg_pyver = set(tags.get('pyver', '').split('.'))
    # we do not check against pkg['python_version'] because some
    # wheels have the Python version in the form major.minor there, and
    # others different version tags separated by - wait for it - a dot!
    # This is very hard - to say the least - to parse correctly.
    for version in versions:
        if version in pkg_pyver:
            return True
    else:
        return False

def _chunk_report(bytes_so_far, chunk_size, total_size):
    if total_size:
        percent = float(bytes_so_far) / total_size
        percent = round(percent * 100, 2)
        print('Downloaded %d of %d bytes (%0.2f%%)' %
            (bytes_so_far, total_size, percent))

        if bytes_so_far >= total_size:
            print('')
    else:
        print('Downloaded %d bytes' % bytes_so_far)

def _chunk_read(response, total_size, report_hook=None, chunk_size=2**15):
    bytes_so_far = 0

    while True:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)

        if not chunk:
            break

        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)

        yield chunk

def _download_package(pkg, verbose=True):
    headers = {'User-Agent' : 'wagenheber.py/%s' % __version__}

    if verbose:
        print("Downloading '%s'..." % pkg['url'])

    response = urllib2.urlopen(urllib2.Request(pkg['url'], headers=headers))
    rinfo = response.info()
    total_size = int(rinfo.get('content-length', 0)) or pkg.get('size')

    if not total_size:
        if verbose:
            print('*Warning*: No total file size available.')

    with tempfile.NamedTemporaryFile('wb', delete=False) as temp:
        for chunk in _chunk_read(response, total_size,
                report_hook=_chunk_report if verbose else None):
            temp.file.write(chunk)

        size = temp.file.tell()

    filename = pkg.get('filename')
    if not filename and 'content-disposition' in rinfo:
        # If PyPI info has no filename, we try to get it from the
        # Content-Disposition header, if present
        try:
            filename = rinfo['content-disposition'].split('filename=')[1]
            if filename[0] == '"' or filename[0] == "'":
                filename = filename[1:-1]
        except Exception:
            filename = None

    if not filename:
        print("Can't determine filename, using 'output'.")
        filename = 'output'

    if size:
        if verbose:
            print("Saving download as '%s'." % filename)
        os.rename(temp.name, filename)
        return filename
    else:
        os.unlink(temp.name)
        PyPiError("Download has zero size. Not saving to file.")

def pypi_download(pkg_name, pkg_ver=None, pkg_type='sdist', py_ver=None,
        verbose=True):
    if not pkg_name:
        raise ValueError("'pkg_name' must be non-null.")

    versions = pypi_versions(pkg_name, None)

    if not versions:
        raise PyPiError("No package named '%s' found." % pkg_name)

    if not pkg_ver:
        pkg_ver = versions[0]
    elif pkg_ver not in versions:
        raise PyPiError('No version %s of package %s available' %
            (pkg_ver, pkg_name))

    pypi = xmlrpclib.ServerProxy(PYPI_URL)
    pkgs = pypi.release_urls(pkg_name, pkg_ver)

    if not pkgs:
        raise PyPiError("No download links for package '%s' "
            "version %s." % (pkg_name, pkg_ver))

    pkgs = [pkg for pkg in pkgs if pkg['packagetype'] == pkg_type
        and _check_py_ver(pkg, py_ver)]

    if not pkgs:
        raise PyPiError("No download links for package '%s' version %s "
            "matching required type '%s' and Python version." %
            (pkg_name , pkg_ver, pkg_type))

    return _download_package(pkgs[0], verbose)

def pypi_versions(pkg_name, limit=10, show_hidden=True):
    if not pkg_name:
        raise ValueError("'pkg_name' must be non-null.")

    pypi = xmlrpclib.ServerProxy(PYPI_URL)
    hits = pypi.package_releases(pkg_name, show_hidden)

    if not hits:
        return []

    if limit and len(hits) > limit:
        hits = hits[:limit]

    return hits

def pypi_search(search_str, limit=0, operator='and'):
    if not search_str:
        raise ValueError("'search_str' must be non-null.")

    pypi = xmlrpclib.ServerProxy(PYPI_URL)
    hits = pypi.search({'name': search_str}, operator)

    if not hits:
        return []

    hits = sorted(hits, key=itemgetter('_pypi_ordering'), reverse=True)

    if limit and len(hits) > limit:
        hits = hits[:limit]

    return hits

def pypi_install_wheel(pkg_name, pkg_ver=None, force=False, verbose=True):
    """Search package on PyPI, download wheel distribution and install it."""
    try:
        filename = pypi_download(pkg_name, pkg_ver, 'bdist_wheel',
            ALLOWED_PY_VER, verbose)
    except Exception as exc:
        try:
            import console
            console.alert("Error", str(exc))
        except ImportError:
            print("Error: %s" % exc)
    else:
        if verbose:
            print("Installing wheel '%s'..." % filename)

        try:
            from wheel import install as winstall
        except ImportError:
            import zipfile

            print("Warning: 'wheel' package not installed. Extracting wheel contents "
                "to 'site-packages' directory...")
            if not os.path.exists('site-packages'):
                os.mkdir('site-packages')
            with zipfile.ZipFile(filename) as z:
                z.extractall('site-packages')
        else:
            whl = winstall.WheelFile(filename)

            try:
                whl.install(force=force)
            except ValueError as exc:
                print("Errors: %s" % exc)

        if verbose:
            print("Done.")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        package = sys.argv[1]
    else:
        try:
            import console
            package = console.input_alert("Package name",
                "Enter name of package to install", '', 'Go')
        except:
            sys.exit(1)

    pypi_install_wheel(package, force=True, verbose=True)
