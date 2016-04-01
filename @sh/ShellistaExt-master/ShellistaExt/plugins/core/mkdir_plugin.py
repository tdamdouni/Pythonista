'''mkdir:
Makes a directory
usage: mkdir directory_name
'''
from .. tools.toolbox import bash
import os

def main(self, line):
    """make a directory"""
    args = bash(line)
    if args is None:
      return
    elif (len(args) == 1):
      target = args[0]
      if os.path.exists(target):
        print "mkdir: %s: File exists" % line
      else:
        try:
          os.mkdir(target)
        except Exception:
          print "mkdir: %s: Unable to create" % line
    else:
      print "mkdir: Usage: mkdir directory_name"
