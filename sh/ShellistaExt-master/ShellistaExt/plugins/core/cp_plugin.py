'''cp:
copy files and directories
usage: cp src [...] dest

'''
alias=['copy']
from .. tools.toolbox import bash
import os,shutil

def main(self, line):
    """copy files and directories"""
    args = bash(line)
    if args is None:
      return
    elif (not (len(args) >= 2)):
      print "cp: Usage: cp src [..] dest"
    else:
      if len(args) > 2:
        files = args[:-1]
        dest = args[-1]
      else:
        files = args[:1]
        dest = args[-1]
      if (len(files) > 1):
        # Copying multiple files, destination must be an existing directory.
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
              if (os.path.isdir(full_file)):
                shutil.copytree(full_file,new_name)
              else:
                shutil.copy(full_file,new_name)
            except Exception:
              print "cp: %s: Unable to copy" % pprint(filef)
      else:
        # Copying a single file to a (pre-existing) directory or a file
        filef = files[0]
        full_file = os.path.abspath(filef).rstrip('/')
        file_name = os.path.basename(full_file)
        full_dest = os.path.abspath(dest).rstrip('/')
        new_name = os.path.join(full_dest,file_name)
        if (os.path.isdir(full_dest)):
          # Destination is a directory already
          if (os.path.exists(full_file)):
            try:
              if (os.path.isdir(full_file)):
                shutil.copytree(full_file,new_name)
              else:
                shutil.copy(full_file,new_name)
            except:
              print "cp: %s: Unable to copy" % pprint(filef)
          else:
            print "cp: %s: No such file" % pprint(filef)
        elif (os.path.exists(full_dest)):
          # Destination is a file
          if (os.path.exists(full_file)):
            try:
              shutil.copy(full_file,full_dest)
            except:
              print "cp: %s: Unable to copy" % pprint(filef)
          else:
            print "cp: %s: No such file" % pprint(filef)
        else:
          if (os.path.isdir(full_file)):
            # Source is a directory, destination should become a directory
            try:
              shutil.copytree(full_file,full_dest)
            except:
              print "cp: %s: Unable to copy" % pprint(filef)
          else:
            # Source is a file, destination should become a file
            try:
              shutil.copy(full_file,full_dest)
            except:
              print "cp: %s: Unable to copy" % pprint(filef)
