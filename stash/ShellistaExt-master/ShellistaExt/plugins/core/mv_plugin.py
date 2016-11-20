'''mv:
Move files and directories
usage: mv file_in_current_dir path_reletive_to_current_dir
'''
from .. tools.toolbox import bash,pprint
import os

def main(self, line):
  """move files and directories"""
  args = bash(line)
  if args is None:
    return
  elif (not (len(args) >= 2)):
    print "mv: Usage: mv src [..] dest"
  else:
    dest  = args[-1]
    files = args[0:-1]
    if (len(files) > 1):
      # Moving multiple files, destination must be an existing directory.
      if (not os.path.isdir(dest)):
        print "cp: %s: No such directory" % pprint(dest)
      else:
        full_dest = os.path.abspath(dest).rstrip('/') + '/'
        for filef in files:
          full_file = os.path.abspath(filef).rstrip('/')
          file_name = os.path.basename(full_file)
          new_name  = os.path.join(full_dest,file_name)
          if (not os.path.exists(full_file)):
            print "! Error: Skipped, missing -", pprint(filef)
            continue
          try:
            os.rename(full_file,new_name)
          except Exception:
            print "mv: %s: Unable to move" % pprint(filef)
    else:
      # Moving a single file to a (pre-existing) directory or a file
      filef = files[0]
      full_file = os.path.abspath(filef).rstrip('/')
      file_name = os.path.basename(full_file)
      full_dest = os.path.abspath(dest).rstrip('/')
      if (os.path.isdir(full_dest)):
        if (os.path.exists(full_file)):
          try:
            os.rename(full_file, full_dest + '/' + file_name)
          except:
            print "mv: %s: Unable to move" % pprint(filef)
        else:
          print "mv: %s: No such file" % pprint(filef)
      else:
        if (os.path.exists(full_file)):
          try:
            os.rename(full_file, full_dest)
          except:
            print "mv: %s: Unable to move" % pprint(filef)
        else:
          print "mv: %s: No such file" % pprint(filef)
