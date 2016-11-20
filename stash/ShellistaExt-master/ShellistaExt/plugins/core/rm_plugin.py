'''rm:
remove one or more files/directories
usage: rm file_or_dir [...]
'''
from .. tools.toolbox import bash,pprint
import os,shutil

alias = ['remove']

def main(self, line):
    """remove one or more files/directories"""
    args = bash(line)
    rflag = False
    if args[0]=='-r':
        rflag = True
        args.pop(0)
    if args is None:
      return
    elif (len(args) < 1):
      print "rm: Usage: rm file_or_dir [...]"
    else:
      for filef in args:
        full_file = os.path.abspath(filef).rstrip('/')
        if not os.path.exists(filef):
          print "! Skipping: Not found -", pprint(filef)
          continue
        if (os.path.isdir(full_file)) and rflag != False:
          try:
            shutil.rmtree(full_file, True)
            if (os.path.exists(full_file)):
              print "rm: %s: Unable to remove" % pprint(filef)
          except Exception:
            print "rm: %s: Unable to remove" % pprint(filef)
        elif args[0] != '.':
          try:
            os.remove(full_file)
          except Exception:
            print "rm: %s: Unable to remove" % pprint(filef)
