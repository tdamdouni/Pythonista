import os
import cmd
import shlex
import importlib
import sys

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

shell = None

CORE_URL='https://github.com/transistor1/shellista-core/archive/master.zip#module_name=plugins&module_path=shellista-core-master&move_to=.'
GIT_URL='https://github.com/transistor1/shellista-git/archive/master.zip#module_name=git&module_path=shellista-git*&move_to=plugins/extensions'
GIT_PLUGIN_GIT='https://github.com/transistor1/shellista-git.git'
CORE_PLUGIN_GIT='https://github.com/transistor1/shellista-core.git'
#CORE_PLUGIN_GIT='https://github.com/transistor1/test-repo.git'
PLUGINS_PLUGIN_GIT='https://github.com/transistor1/shellista-plugins.git'

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

#Download plugins
def _check_for_plugins():
    plugins_parent = os.path.join(os.path.dirname(__file__))
    plugins_dir = os.path.join(plugins_parent, 'plugins')
    extensions_dir = os.path.join(plugins_dir,'extensions')
    git_dir = os.path.join(extensions_dir,'git')
    plugins_plugin_dir = os.path.join(extensions_dir,'plugins')

    if not os.path.exists(plugins_dir):
        print 'Downloading plugins...'
        #Do not create plugins folder yet, bootstrapping core will do that

        #Bootstrap core module - it is needed by Git
        installer = ModuleInstaller(CORE_URL)
        installer.module_install()

        #Create plugins/extensions
        os.makedirs(extensions_dir)

        #Create __init__.py files
        installer._touch_file(os.path.join(extensions_dir, '__init__.py'))
        installer._touch_file(os.path.join(plugins_dir, '__init__.py'))
        installer._touch_file(os.path.join(plugins_parent, '__init__.py'))

        #Now bootstrap the Git module
        installer = ModuleInstaller(GIT_URL)
        installer.module_install()

        #Clone the core repo to make it eligible for upgrades
        global git
        import plugins.extensions.git.git_plugin as git

        with _context_chdir(plugins_dir):
            try:
                _do_clone(CORE_PLUGIN_GIT)
            except:
                print 'Couldn\'t git clone core (already cloned?)'

        #Clone the plugins repo
        os.mkdir(plugins_plugin_dir)
        with _context_chdir(plugins_plugin_dir):
            _do_clone(PLUGINS_PLUGIN_GIT)

        #Clone git to make it eligible for update
        with _context_chdir(git_dir):
            _do_clone(GIT_PLUGIN_GIT)

def _do_clone(url):
    git.do_git('clone {0}'.format(url))

@contextlib.contextmanager
def _context_chdir(new_path):
    '''Change directories, saving the old path. To be used in
         a with statement'''
    os._old_path = os.getcwd()
    os.chdir(new_path)
    yield
    os.chdir(os._old_path)

class Shellista(cmd.Cmd):
    PRECMD_PLUGINS = []
    POSTCMD_PLUGINS = []

    #TODO: Use ConfigParser to set initial values, add
    #    plugin to manage settings
    settings = {}

    def __init__(self, stdin=sys.stdin, stdout=sys.stdout):
        self.did_quit = False
        self.cmdList = ['quit','exit','logoff','logout',]
        #self._bash = BetterParser()
        #self._bash.env_vars['$HOME']   = os.path.expanduser('~/Documents')
        for root,directory,files in os.walk('./plugins'):#os.listdir(os.path.join(os.curdir,'plugins')):

            for file in files:
                (path, extension) = os.path.splitext(file)

                if extension == '.py' and path != '__init__' and '_plugin' in path:
                    self._hook_plugin_main(root, path)

        cmd.Cmd.__init__(self, stdin=stdin, stdout=stdout)
        try:
            import editor
            os.chdir(os.path.dirname(editor.get_path()))
        except Exception:
            try:
                os.chdir(os.path.dirname(sys.argv[0]))
            except Exception:
                os.chdir(os.path.expanduser('~'))
        self.getPrompt()

    def _hook_plugin_main(self, root, path):
        #Change directory, changing back to old dir when finished
        with _context_chdir(os.path.dirname(os.path.abspath(__file__))):
            try:
                lib = None

                #Strip path.
                #TODO: Remove filesystem-specific path stuff
                if root[:2] == './':
                    root = root[2:]

                lib = importlib.import_module(root.replace('/','.') + '.' + path)
                name = 'do_' + path.lower().replace('_plugin','')
                if self.addCmdList(path.lower()):
                    setattr(Shellista, name, self._CmdGenerator(lib.main))

                try:
                    for a in lib.alias:
                    #pass
                        if self.addCmdList(a):
                            parent = path.lower().replace('_plugin','')
                            setattr(Shellista,'do_' + a.lower(),self._aliasGenerator(getattr(self,name)))
                            setattr(Shellista,'help_' + a.lower(),self._HelpGenerator('Alias for: %s. Please use help on %s for usage.' % (parent,parent)))

                except (ImportError, AttributeError) as desc:
                    pass
                try:
                    for hook in lib.precmdhook:
                        self.precmd_plugin(hook)
                except (AttributeError) as desc:
                    pass
                try:
                    for hook in lib.postcmdhook:
                        self.postcmd_plugin(hook)
                except (AttributeError) as desc:
                    pass


                if lib.__doc__:
                    setattr(Shellista, 'help_' + path.lower().replace('_plugin',''), self._HelpGenerator(lib.__doc__))
            except (ImportError, AttributeError) as desc:
                print('Exception error: ' + lib.__name__ if lib else '')
                print(desc)
                #raise

    def bash(self, argstr):
        try:
            return self._bash.parse('. ' + argstr)[1:]
        except SyntaxError, e:
            print "Syntax Error: %s" % e
            return None

    def _CmdGenerator(self, function):
        def CmdProxy(self, line):
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
            self.prompt = '<~ > '
        else:
            self.prompt = '<~/'+prompt + ' > '

    def emptyline(self):
        pass

if __name__ == '__main__':
    if not shell:
        _check_for_plugins()
        shell = Shellista()
        shell.cmdloop()
