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

PLUGINS_URL='https://github.com/briarfox/ShellistaExt/archive/master.tar.gz#module_name=plugins&module_path=ShellistaExt-master/ShellistaExt/plugins&move_to=.'

#Imports for ModuleInstaller
import mimetypes
import tarfile
import zipfile
import urllib2
import contextlib
import shutil
import glob
import urlparse

class ModuleInstaller():
  url = ''
  mime_type = None
  download_name = ''
  module_path = ''
  move_to = ''
  working_dir = '.'
  module_name = ''
  install_root = ''

  def __init__(self, url, working_dir='./.module_installer'):
    '''Initialize ModuleInstaller.  Url should contain a fragment (#) with
    :param url: URL of file to install
    query parameters:
    http(s)://url/file.tar.gz#module_name=modname&module_path=Some/Path&move_to=/
    module_name = local name of the module
    module_path = relative path, once the module has been extracted, to the module dir to "install".
    move_to = path to extract the module to, relative to install_root
    '''
    mimetypes.init()

    self.url = url
    parsed_url = urlparse.urlparse(url)
    qs = urlparse.parse_qs(parsed_url.fragment)

    if not qs.get('module_name') or not qs.get('module_path') or not qs.get('move_to'):
      raise Exception('ModuleInstaller: Missing query string parameters')

    self.module_path = qs['module_path'][0]
    self.move_to = qs['move_to'][0]
    self.mime_type = mimetypes.guess_type(parsed_url.path)
    self.working_dir = os.path.abspath(working_dir)
    self.module_name = qs['module_name'][0]

    ext = os.path.splitext(parsed_url.path)
    ext = os.path.splitext(ext[0])[1] + ext[1] #In case it's a .tar.gz
    
    self.download_name = self.module_name + ext
    self.install_root = os.getcwd()

  def untgz(self, name, to='.'):
    tfile = tarfile.open(name, 'r:gz')
    tfile.extractall(to)

  def unzip(self, name, to='.'):
    zfile = zipfile.ZipFile(name)
    zfile.extractall(to)

  #From mark_harris' wget
  def download(self, url, dst=None):
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
    except Exception as e:
      print 'Download error: ', e

  def _mkworkdir(self):
    '''Create the working directory'''
    if not os.path.exists(self.working_dir):
      os.mkdir(self.working_dir)

  def _rmworkdir(self):
    '''Remove the working directory'''
    if os.path.exists(self.working_dir):
      shutil.rmtree(self.working_dir)

  def _glob_expand_path(self, glob_path):
    '''Return the first glob matched entry'''
    glob_result = glob.glob(glob_path)
    if len(glob_result) > 0:
      return glob_result[0]

  def _workpath(self, *args):
    '''Helper to get a subfolder of working path'''
    return os.path.join(self.working_dir, *args)

  def module_install(self):
    '''Module "installer" for pure Python modules.'''
    
    self._mkworkdir()
    
    self.download(self.url, self._workpath(self.download_name))
    
    extract_func =  {
                      ('application/x-tar', 'gzip'): self.untgz,
                      ('application/zip', None): self.unzip,
                    }[self.mime_type]
                    
    extract_func(self._workpath(self.download_name), self._workpath())
    
    module_full_path = self._workpath(self.module_path)
    
    src = self._glob_expand_path(module_full_path)
    move_to = self.move_to
    
    #Strip leading slash, if any
    if move_to.startswith(os.pathsep):
      move_to = move_to[1:]
      
    dst = os.path.join(self.install_root, self.move_to)
    
    #Move the source folder to the dest
    os.rename(src, os.path.join(dst, os.path.basename(src)))
    
    self._rmworkdir() #Clean up

#Download plugins
def _check_for_plugins():
 plugins_parent = os.path.join(os.path.dirname(__file__))
 if not os.path.exists(os.path.join(plugins_parent, 'plugins')):
  print 'Downloading plugins...'
  installer = ModuleInstaller(PLUGINS_URL)
  installer.module_install()
 
class Shellista(cmd.Cmd):
  
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
                        print('Exption error')
                        print(desc)

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
       
    def _CmdGenerator(self,function):
        def CmdProxy(self, line):
            #args = [name]
            #args.extend(shlex.split(line))
            function(self,line)
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
        
    def postcmd(self,stop,line):
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

_check_for_plugins()
shell = Shellista()
shell.cmdloop()
