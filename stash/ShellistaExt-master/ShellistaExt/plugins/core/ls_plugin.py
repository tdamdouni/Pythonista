'''Lists files directory'''

from .. tools.toolbox import bash,pprint

import os

def main(self, line):
    """list directory contents"""
    files = bash(line)
    if files is None:
      return
    elif (not files):
      files = ['.']
    files_for_path = dict()
    for filef in files:
      full_file = os.path.abspath(filef).rstrip('/')
      file_name = os.path.basename(full_file)
      dir_name  = os.path.dirname(full_file).rstrip('/')
      if (not os.path.exists(full_file)):
        print "! Error: Skipped, missing -", pprint(filef)
        continue
      if (os.path.isdir(full_file)):
        # Need to add this as a key and all the files contained inside it
        _dirs = files_for_path.get(full_file, set())
        for new_file in os.listdir(full_file):
          _dirs.add(full_file.rstrip('/') + '/' + new_file.rstrip('/'))
        files_for_path[full_file] = _dirs
      else:
        _dirs = files_for_path.get(dir_name, set())
        _dirs.add(full_file)
        files_for_path[dir_name] = _dirs
    # Iterate over the paths, in alphabetical order:
    paths = sorted(files_for_path.keys())
    cwd = os.getcwd().rstrip('/')
    in_cwd = False
    if (cwd in paths):
      # Move cwd to the front, mark that it's present
      paths.remove(cwd)
      paths = [cwd] + paths
      in_cwd = True
    for i,path in enumerate(paths):
      if (i > 0):
        print "\n" + pprint(path) + "/:"
      elif (not in_cwd):
        print pprint(path) + "/:"
      for filef in sorted(list(files_for_path[path])):
        full_file = os.path.abspath(filef).rstrip('/')
        file_name = os.path.basename(full_file)
        if (os.path.isdir(full_file)):
          print file_name + "/"
        else:
          print file_name + (" (%s)" % (sizeof_fmt(os.stat(full_file).st_size)))


def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
      if num < 1024.0:
        if (x == 'bytes'):
          return "%s %s" % (num, x)
        else:
          return "%3.1f %s" % (num, x)
      num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
