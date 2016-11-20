import os
import cmd
import shlex
import importlib

# Credits
#
# The python code here was written by pudquick@github and modified by briarfox@github
#
# License
#
# This code is released under a standard MIT license.
#
#   Permission is hereby granted, free of charge, to any person
#   obtaining a copy of this software and associated documentation files
#   (the "Software"), to deal in the Software without restriction,
#   including without limitation the rights to use, copy, modify, merge,
#   publish, distribute, sublicense, and/or sell copies of the Software,
#   and to permit persons to whom the Software is furnished to do so,
#   subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
#   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
#   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

# You can skip over reading this class, if you like.
# It's an implementation of mine of the bash parser in pure python
# This has advantages over shlex, glob, and shlex->glob in that it expects
# the strings to represent files from the start.

#PLUGINS_URL='https://github.com/briarfox/ShellistaExt/archive/master.tar.gz#module_name=plugins&module_path=ShellistaExt-master/ShellistaExt/plugins&move_to=.'

#PLUGINS_URL='https://github.com/transistor1/shellista-hybrid/archive/master.tar.gz#module_name=plugins&module_path=shellista-hybrid-master/plugins&move_to=.'

#PLUGINS_URL='https://github.com/transistor1/shellista/archive/master.tar.gz#module_name=plugins&module_path=shellista-master&move_to=./plugins'

shell = None

__DEBUG__ = False

if __DEBUG__:
    base_url = 'file:///{0}/{1}/{2}'.format(os.path.dirname(os.getcwd()),'shellista-deps','{0}')
    PLUGINS_URL= base_url.format('ShellistaExt-master.tar.gz#module_name=plugins&module_path=ShellistaExt/ShellistaExt/plugins&move_to=.')
else:
    #PLUGINS_URL='https://github.com/briarfox/ShellistaExt/archive/master.tar.gz#module_name=plugins&module_path=ShellistaExt-master/ShellistaExt/plugins&move_to=.'
    PLUGINS_URL='https://github.com/transistor1/ShellistaExt/archive/dev-modular.zip#module_name=plugins&module_path=ShellistaExt-*/ShellistaExt/plugins&move_to=.'


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
    full_install_path = '' #Absolete path to move_to
    
    def __init__(self, url, working_dir='./.module_installer', root_dir=None):
        '''Initialize ModuleInstaller.  Url should contain a fragment (#) with
        :param url: URL of file to install
        query parameters:
        http(s)://url/file.tar.gz#module_name=modname&module_path=Some/Path&move_to=/
        module_name = local name of the module
        save_as = force download to save as name
        module_path = relative path, once the module has been extracted, to the module dir to "install" (copy the folder/file to the move_to path)
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
        
        #module = __import__(modulename, globals(), locals())
        #globals()[modulename]=module
        #sys.modules[modulename] = module
        
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
        if len(glob_result) > 0:
            return glob_result[0]

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

    def module_install(self, progress_func=None, overwrite_existing=False):
        '''Module "installer" for pure Python modules.'''
        try:
            #If the work dir already exists, delete it.
            self._rmworkdir()
            
            #Remake the work dir
            self._mkworkdir()
            
            self.download(self.url, self._workpath(self.download_name), progress_func)

            extract_func =  {
                              ('application/x-tar', 'gzip'): self.untgz,
                              ('application/zip', None): self.unzip,
                              ('text/x-python', None): None,
                            }[self.mime_type]

            if extract_func:
                extract_func(self._workpath(self.download_name), self._workpath())
            module_full_path = self._workpath(self.module_path)

            src = self._glob_expand_path(module_full_path)
            #move_to = self.move_to

            #Strip leading slash, if any
            #if move_to.startswith(os.pathsep):
            #    move_to = move_to[1:]
            
            #Absolute path where the modules will be installed
            #dst = os.path.join(self.install_root, self.move_to)
            
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
        except Exception as e:
            raise ModuleDownloadException(e)

#Download plugins
def _check_for_plugins():
    plugins_parent = os.path.join(os.path.dirname(__file__))
    plugins_dir = os.path.join(plugins_parent, 'plugins')
    if not os.path.exists(plugins_dir):
        print 'Downloading plugins...'
        #os.mkdir('plugins')
        installer = ModuleInstaller(PLUGINS_URL)
        installer.module_install()

class Shellista(cmd.Cmd):
    PRECMD_PLUGINS = []
    POSTCMD_PLUGINS = []

    #TODO: Use ConfigParser to set initial values, add
    #       plugin to manage settings
    settings = {}

    def __init__(self):
        self.did_quit = False
        self.cmdList = ['quit','exit','logoff','logout',]
        #self._bash = BetterParser()
        #self._bash.env_vars['$HOME']   = os.path.expanduser('~/Documents')
        for root,directory,files in os.walk('./plugins'):#os.listdir(os.path.join(os.curdir,'plugins')):

            for file in files:
                (path, extension) = os.path.splitext(file)

                if extension == '.py' and path != '__init__' and '_plugin' in path:
                    try:

                        lib = importlib.import_module(root[2:].replace('/','.')+'.'+path)
                        name = 'do_'+path.lower().replace('_plugin','')
                        if self.addCmdList(path.lower()):
                            setattr(Shellista, name, self._CmdGenerator(lib.main))

                        try:
                            for a in lib.alias:
                            #pass
                                if self.addCmdList(a):
                                    parent = path.lower().replace('_plugin','')
                                    setattr(Shellista,'do_' + a.lower(),self._aliasGenerator(getattr(self,name)))
                                    setattr(Shellista,'help_'+a.lower(),self._HelpGenerator('Alias for: %s. Please use help on %s for usage.' % (parent,parent)))

                        except (ImportError, AttributeError) as desc:
                            pass



                        if lib.__doc__:
                            setattr(Shellista, 'help_' + path.lower().replace('_plugin',''), self._HelpGenerator(lib.__doc__))
                    except (ImportError, AttributeError) as desc:
                        print('Exception error: ' + lib.__name__ if lib else '')
                        import traceback
                        traceback.print_exc()
                        #traceback.print_tb(sys.exc_traceback)
                        #print(desc)


        cmd.Cmd.__init__(self)
        os.chdir(os.path.expanduser('~/Documents'))
        self.getPrompt()

    def bash(self, argstr):
        try:
            #print self._bash.parse('. ' + argstr)[1:]
            return self._bash.parse('. ' + argstr)[1:]
        except SyntaxError, e:
            print "Syntax Error: %s" % e
            return None

    def _CmdGenerator(self, function):
        def CmdProxy(self, line):
            #args = [name]
            #args.extend(shlex.split(line))
            function(self, line)
            self.getPrompt()

        return CmdProxy

    def _HelpGenerator(self, help):
        def HelpProxy(self):
            print(help)

        return HelpProxy

    def _aliasGenerator(self,func):

        def aliasProxy(self,line):

            func(line)
        return aliasProxy

    def do_quit(self,line):
        self.did_quit = True

    def do_exit(self,line):
        self.did_quit = True
    def do_close(self,line):
        self.did_quit = True
    def do_logout(self,line):
        self.did_quit = True
    def do_logoff(self,line):
        self.did_quit = True

    @classmethod
    def precmd_plugin(cls, func):
        cls.PRECMD_PLUGINS.append(func)
        print cls.PRECMD_PLUGINS
    
    @classmethod    
    def postcmd_plugin(cls, func):
        cls.POSTCMD_PLUGINS.append(func)

    def precmd(self, line):
        plugins = self.PRECMD_PLUGINS
        for plugin in plugins:
            line = plugin(self, line)
        line = cmd.Cmd.precmd(self, line)
        return line
        
    def postcmd(self, stop, line):
        plugins = self.POSTCMD_PLUGINS
        for plugin in plugins:
            plugin(self, stop, line)
        return self.did_quit

    def addCmdList(self,name):
        if name in self.cmdList:
            print 'Conflict: Command %s already in use.' % name
            return False
        else:
            self.cmdList.append(name)
            return True







    def getPrompt(self):
        prompt = os.path.relpath(os.getcwd(),os.path.expanduser('~'))
        if prompt == '.':
            self.prompt = '</ >'
        else:
            self.prompt = '</'+prompt + ' >'

    def emptyline(self):
        pass

if __name__ == '__main__':
    if not shell:
        _check_for_plugins()
        shell = Shellista()
        shell.cmdloop()
    

