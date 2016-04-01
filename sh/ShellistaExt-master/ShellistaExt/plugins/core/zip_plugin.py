'''zip:
zips a directory
usage: zip some/directory
'''
from .. tools.toolbox import bash,pprint
import zipfile,os

def main(self, line):
    args = bash(line)
    path = os.getcwd() +'/'+ args[0]
    name = args[0]+'.zip'
    relroot = os.path.abspath(os.path.join(path, os.pardir))

    with zipfile.ZipFile(name, "w",zipfile.ZIP_DEFLATED) as zip:
      for root, dirs, files in os.walk(path):
        # add directory (needed for empty dirs)
        zip.write(root, os.path.relpath(root, relroot))
        for file in files:
          filename = os.path.join(root, file)
          print pprint(filename)
          if os.path.isfile(filename): # regular files only
            arcname = os.path.join(os.path.relpath(root, relroot), file)
            zip.write(filename, arcname)
      zip.close()
