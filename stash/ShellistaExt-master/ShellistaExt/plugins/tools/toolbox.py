from betterParser import BetterParser
import os

_bash = BetterParser()
_bash.env_vars['$HOME']   = os.path.expanduser('~/Documents')

def bash(argstr):
  try:
    #print self._bash.parse('. ' + argstr)[1:]
    return _bash.parse('. ' + argstr)[1:]
  except SyntaxError, e:
    print "Syntax Error: %s" % e
  return None
  
def pprint(path):
  #HOME = os.path.expanduser('~/Documents')
  if (path.startswith(_bash.env_vars['$HOME'])):
    return '~' + path.split(_bash.env_vars['$HOME'],1)[-1]
  return path
