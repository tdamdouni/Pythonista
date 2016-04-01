# coding: utf-8
import requests
import zipfile
import tarfile
import shutil
import os
try:
    import xmlrpclib
except ImportError:
    import xmlrpclib.client as xmlrcplib
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO  import StringIO

installdir     = os.path.expanduser("~/Documents/site-packages")
client         = xmlrpclib.ServerProxy("https://pypi.python.org/pypi")
SUPPORTED_EXTS = [
    ".zip",
    ".tar.gz"
]


class PypiError(Exception): pass
class PackageError(PypiError): pass
class UnsupportedExtension(PackageError): pass

def can_unpack(url):
    """ Check if url can be unpacked (.zip or .tar.gz)
    """
    for ext in SUPPORTED_EXTS:
        if url["url"].endswith(ext): return True

def download(pkgname):
    releases = client.package_releases(pkgname)
    if not releases:
        raise PackageError("package '{}' not found".format(pkgname))
    
    release = releases[0]
    geturls = client.release_urls(pkgname, release)
    geturls = [url for url in geturls if can_unpack(url)]
    if not geturls:
        raise PackageError(
            "no downloads available for package '{}'".format(pkgname))
    url = geturls[0]["url"]
    return requests.get(url).content, url

def install_targz(io, name, file, installdir=installdir):
    zp = tarfile.open(fileobj=io, mode="r:gz")
    zp.extractall(installdir)
    master = zp.getnames()[0]
    if file:
        imaster = os.path.join(installdir, master)
        shutil.move(os.path.join(imaster, file), installdir)
        shutil.rmtree(imaster)
    io.close()

def install_zip(io, file, installdir=installdir):
    zp = zipfile.ZipFile(io)
    zp.extractall(installdir)
    master = zp.namelist()[0]
    if file:
        imaster = os.path.join(installdir, master)
        shutil.move(os.path.join(imaster, file), installdir)
        shutil.rmtree(imaster)
    io.close()
    
def install(data, name, file=None, installdir=installdir):
    """ Install package
    data       - archive data
    name       - archive filename
    file       - file to install/extract
    installdir - directory where package should be installed
    """
    io = StringIO(data)
    if name.endswith(".zip"):
        install_zip(io, file, installdir)
    elif name.endswith(".tar.gz"):
        install_targz(io, name, file, installdir)
    else:
        io.close()
        raise UnsupportedExtension(name)
