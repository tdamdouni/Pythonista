
import os,sys

#DULWICH_URL='https://github.com/jelmer/dulwich/archive/master.tar.gz#module_name=dulwich&module_path=dulwich-master/dulwich&move_to=site-packages'
GITTLE_URL='https://github.com/jsbain/gittle/archive/master.tar.gz#module_name=gittle&module_path=gittle-*/gittle&move_to=site-packages'
FUNKY_URL='https://github.com/FriendCode/funky/archive/master.tar.gz#module_name=funky&module_path=funky*/funky&move_to=site-packages&save_as=funky.tar.gz'

DULWICH_URL='https://github.com/jsbain/dulwich/archive/master.tar.gz#module_name=dulwich&module_path=dulwich-master/dulwich&move_to=site-packages'

def _progress(tot):
    print 'Downloaded {0} bytes'.format(tot)
    
def main():
    #Make sure you order these in terms of what is needed first
    for i in [FUNKY_URL, DULWICH_URL, GITTLE_URL]:
        installer = ModuleInstaller(i, 
            root_dir=os.path.expanduser('~/Documents'))
        print "Importing " + installer.module_name
        #installer.try_import_or_install(overwrite_existing=True, progress_func=_progress)
        installer.module_install(overwrite_existing=True, progress_func=_progress)


#Imports for ModuleInstaller
import mimetypes
import tarfile
import zipfile
import urllib2
import contextlib
import shutil
import glob
import urlparse
import os
import sys
import importlib

#Thin wrapper around Exception
class ModuleDownloadException(Exception):
    pass

class ModuleInstaller():
    url = '' #Download URI
    mime_type = None #Mime type of downloaded file
    download_name = '' #Local download name
    module_path = '' #Relative install path of module
    move_to = '' #Move module to folder relative to install_root
    working_dir = '' #Work is done in this folder
    module_name = '' #Local name of module
    install_root = '' #Root folder where ModuleInstaller starts from
    full_install_path = '' #Absolute path to move_to

    def __init__(self, url, working_dir='./.module_installer', root_dir=None):
        '''Initialize ModuleInstaller.  Url should contain a fragment (#) with
        :param url: URL of file to install
        query parameters:
        http(s)://url/file.tar.gz#module_name=modname&module_path=Some/Path&move_to=/
        module_name = local name of the module
        save_as = force download to save as name
        module_path = relative path, once the module has been extracted, to the
         module dir to "install" (copy the folder/file to the move_to path)
        move_to = path to extract the module to, relative to install_root
        '''
        mimetypes.init()

        self.url = url
        parsed_url = urlparse.urlparse(url)
        qs = urlparse.parse_qs(parsed_url.fragment)

        #Make sure required query params exist
        if not qs.get('module_name') \
            or not qs.get('module_path') \
            or not qs.get('move_to'):
            raise ModuleDownloadException('ModuleInstaller: Missing query string parameters')

        self.module_path = qs['module_path'][0]
        self.move_to = qs['move_to'][0]
        self.mime_type = mimetypes.guess_type(parsed_url.path)
        self.working_dir = os.path.abspath(working_dir)
        self.module_name = qs['module_name'][0]

        ext = os.path.splitext(parsed_url.path)
        ext = os.path.splitext(ext[0])[1] + ext[1] #In case it's a .tar.gz

        save_as = qs.get('save_as')
        self.download_name = save_as[0] if save_as else self.module_name + ext

        #Try to get the mime type from save_as name, if one doesn't exist
        if not self.mime_type[0]:
            self.mime_type = mimetypes.guess_type(self.download_name)

        self.install_root = root_dir if root_dir else os.getcwd()

        #Absolute path where the modules will be installed
        self.full_install_path = os.path.join(self.install_root, self.move_to)

    def _global_import(self, modulename):
        module = importlib.import_module(modulename)
        globals()[modulename] = module

    def _get_file_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    def _mkworkdir(self):
        '''Create the working directory'''
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)

    def _rmworkdir(self):
        '''Remove the working directory'''
        if os.path.exists(self.working_dir):
            shutil.rmtree(self.working_dir)

    def _touch_file(self, path):
        with open(path, 'w') as touch:
            pass

    def _glob_expand_path(self, glob_path):
        '''Return the first glob matched entry'''
        glob_result = glob.glob(glob_path)
        if len(glob_result) == 1:
            return glob_result[0]
        else:
            raise ModuleDownloadException('Ambiguous path match detected: {0}'.format(glob_path))

    def _workpath(self, *args):
        '''Helper to get a subfolder of working path'''
        return os.path.join(self.working_dir, *args)

    def _add_module_path(self):
        '''Add the installed module path to sys.path'''
        mod_path = self.full_install_path + os.sep
        if not os.path.exists(mod_path):
            os.makedirs(mod_path)

        if not mod_path in sys.path:
            sys.path.insert(0, self.full_install_path + os.sep)

    def untgz(self, name, to='.'):
        tfile = tarfile.open(name, 'r:gz')
        tfile.extractall(to)

    def unzip(self, name, to='.'):
        zfile = zipfile.ZipFile(name)
        zfile.extractall(to)

    def try_import(self):
        self._add_module_path()
        self._global_import(self.module_name)

    def try_import_or_install(self, progress_func=None, overwrite_existing=False):
        '''Try to import the module. Failing that, download it.'''
        try:
            self.try_import()
        except ImportError:
            self.module_install(progress_func, overwrite_existing)
            self.try_import()

    #From mark_harris' wget
    def download(self, url, dst=None, progress_func=None):
        '''Download a file from url, optionally naming it locally'''
        if not dst:
            os.path.basename(url.split('?',1)[0])
        try:
            total=0
            with contextlib.closing(urllib2.urlopen(url)) as c:
                with open(dst,'wb') as f:
                    while True:
                        data=c.read(32*1024)
                        if data=='':
                            break
                        f.write(data)
                        total+=len(data)
                        if progress_func:
                            progress_func(total)
        except Exception as e:
            raise ModuleDownloadException(e)
            #print 'Download error: ', e

    def module_install(self, progress_func=None, overwrite_existing=False,
                       post_install_hook=None):
        '''Module "installer" for pure Python modules.
            :param progress_func: A callback function to display progress
            :param overwrite_existing: A boolean to indicate whether to overwrite existing
                destination
            :param post_install_hook: A callback to do install-specific
                things after the install
        '''
        try:
            #If the work dir already exists, delete it.
            self._rmworkdir()

            #Remake the work dir
            self._mkworkdir()

            self.download(self.url, self._workpath(self.download_name), progress_func)

            extract_func = {
                              ('application/x-tar', 'gzip'): self.untgz,
                              ('application/zip', None): self.unzip,
                              ('text/x-python', None): None,
                            }[self.mime_type]

            #If there is an extraction function for the filetype, call it
            if extract_func:
                extract_func(self._workpath(self.download_name), self._workpath())

            #Get the full path to the extracted module
            module_full_path = self._workpath(self.module_path)

            #Expand any wildcards in module_path
            src = self._glob_expand_path(module_full_path)
            
            print src
            #Rename module folder
            if os.path.isdir(src) and os.path.basename(src) != self.module_name:
                new_name = os.path.join(os.path.dirname(src), self.module_name)
                os.rename(src, new_name)
                src = new_name

            dst = self.full_install_path

            if not os.path.exists(dst):
                os.makedirs(dst)


            try:
                if overwrite_existing:
                    existing = os.path.join(dst, os.path.basename(src))
                    if os.path.exists(existing):
                        if os.path.isdir(existing):
                            shutil.rmtree(existing)
                        else:
                            os.unlink(existing)


                #Move the source folder to the dest
                shutil.move(src, os.path.join(dst, os.path.basename(src)))
            except Exception as e:
                raise e
                raise ModuleDownloadException('Module: {0} - Can\'t find directory module_path. Please check that the module was extracted correctly, and into the proper directory.'.format(self.module_name))

            self._rmworkdir()

            if post_install_hook:
                post_install_hook(self)

        except Exception as e:
            raise ModuleDownloadException(e)
if __name__=='__main__':
    main()
