'''cat:
Prints a file
'''
#__package__ = 'plugins.extensions'
#from .. extensions.ed import ed
from ... tools.toolbox import bash
import os
from . import ed

def main(self, line):
    """print file"""
    args = bash(line)
    if args is None:
      e=ed.ed()
    elif (len(args) != 1):
        print 'usage: ed file'
    else:
      target = args[0]
      if (not os.path.exists(target)):
        print "cat: %s: No such file" % line
      elif (os.path.isdir(target)):
        print "cat: %s: Is a directory" % line
      else:
        e=ed.ed(target)
