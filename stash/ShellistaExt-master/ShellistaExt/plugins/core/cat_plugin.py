'''cat:
Prints a file
'''
#__package__ = 'ShellistaExt.plugins.core'
from .. tools.toolbox import bash
import os


def main(self, line):
    """print file"""
    args = bash(line)
    if args is None:
      return
    elif (len(args) != 1):
      print "cat: Usage: cat file"
    else:
      target = args[0]
      if (not os.path.exists(target)):
        print "cat: %s: No such file" % line
      elif (os.path.isdir(target)):
        print "cat: %s: Is a directory" % line
      else:
        try:
          contents = ""
          with open(target, 'r') as f:
            contents = f.read()
          print contents
          print ""
        except Exception:
          print "cat: %s: Unable to access" % line
