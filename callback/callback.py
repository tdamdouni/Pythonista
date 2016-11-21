import urllib
import inspect
import os
import json
import functools

URL_BASE = "pythonista://"

def current_script():
    '''Returns name of the script that was executed'''
    return os.path.splitext(os.path.split(inspect.stack()[-1][1])[1])[0]

def url(cmd,script=None,**kw):
    '''
    Returns a callback URL for the specified command and keyword arguments
    If script is not specified, the current one is used.
    '''
    if not script: 
        script = current_script()
    kw['cmd'] = cmd
    a = URL_BASE + urllib.quote(script) + '?action=run'
    a += "&argv=callback&argv=" + urllib.quote(json.dumps(kw))
    return a

def get_info(args):
    '''
    Returns a dictionary with the script arguments by parsing the passed argv
    and the command name as the 'cmd' key.
    '''
    if len(args) > 1 and args[1] == 'callback':
      try:
          return json.loads(args[2])
      except ValueError:
          return None #silently fail if the JSON payload is invalid
    return None

class UnhandledCommandException(Exception):
    '''Exception thrown when a command is not registered to a handler'''
    def __init__(self,cmdname):
       Exception.__init__(self,"%s was not handled." % cmdname)

class InfoHandler(object):
    '''Simple class to wrap callback command handling'''
    def __init__(self,args):
        '''Constructs InfoHandler with the specified argv'''
        self.args = get_info(args)
        self.cmdmap = {}
    def cmd(self,cmdname):
        '''
        Decorator which registers the wrapped function 
        as a handler for the specified cmdname
        '''
        def deco(f):
            self.cmdmap[cmdname] = f
            return f
        return deco
    def handle(self):
        '''
        Handle the given arguments and return True if there was a command to handle.
        This should be called after all commands are registered with the cmd decorator.
        '''
        if not self.args: return False #not a callback
        cmdname = self.args['cmd']
        if cmdname not in self.cmdmap:
            raise UnhandledCommandException(cmdname)
            return True
        del self.args['cmd']
        self.cmdmap[cmdname](**self.args)
        return True
