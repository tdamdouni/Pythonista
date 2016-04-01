'''ungzip:
unzip a gzip archive
usage: ungzip file [destination]
'''
from .. tools.toolbox import bash,pprint

import os,shutil, zipfile, tarfile, gzip,glob

alias = ['gunzip']
def main(self, line):
  """ungzip a gzip archive"""
        # filename with optional output filename
  fname = 'ungzip'
  #if gunzip:
   #   fname = 'gunzip'
  args = bash(line)
  if args is None:
      return
  elif not (1 <= len(args) <= 2):
      print "%s: Usage: %s file [outfile]" % (fname, fname)
  else:
      filename = os.path.abspath(args[0])
      if not os.path.isfile(filename):
          print "%s: %s: No such file" % (fname,args[0])
      else:
          # '\x1f\x8b\x08' magic marker check
          f = open(filename, 'rb')
          try:
              gz_check = f.read(3)
          except Exception:
              gz_check = ''
          finally:
              f.close()
          if gz_check != '\x1f\x8b\x08':
              print "%s: %s: does not appear to be a gzip file" % (fname,args[0])
          else:
              if (os.path.basename(filename).lower().endswith('.gz') or os.path.basename(filename).lower().endswith('.gzip')):
                  altpath = os.path.splitext(os.path.basename(filename))[0]
              elif os.path.basename(filename).lower().endswith('.tgz'):
                  altpath = os.path.splitext(os.path.basename(filename))[0] + '.tar'
              else:
                  altpath = os.path.basename(filename) + '_ungzipped'
              altpath = os.path.join(os.path.dirname(filename), altpath)
              location = (args[1:2] or [altpath])[0]
              if os.path.exists(location):
                  print "%s: %s: destination already exists" % (fname,os.path.basename(location))
                  return                    
              dirf = os.path.dirname(os.path.dirname(os.path.abspath(location)))
              try:
                  if not os.path.exists(dirf):
                      os.makedirs(dirf)
                  with open(location, 'wb') as outfile:
                      with gzip.open(filename, 'rb') as gzfile:
                          outfile.write(gzfile.read())
              except Exception, error:
                  print error.__doc__
                  print error.message
                  print "%s: %s: gzip file is corrupt" % (fname, args[0])
           
if __name__ == '__main__':
  os.chdir(os.path.expanduser('~/Documents'))
  main('bottle-0.12.7.tar.gz')
