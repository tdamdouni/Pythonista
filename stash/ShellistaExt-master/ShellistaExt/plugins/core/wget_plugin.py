'''wget: downloads a file from a url'''

import urllib2,os,sys
from .. tools.toolbox import bash

alias = ['get',]

def main(self, line):
  '''Gets a file from a link.'''
  args = bash(line)
  if args == None:
    return
  if len(args)==1:
    file_name,ext = os.path.splitext(args[0].split('/')[-1])
    try:
      u = urllib2.urlopen(args[0])
    except :
      print 'Invalid url'
    f = open(file_name+ext, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name+ext, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
      #pr
      buffer = u.read(block_sz)
      if not buffer:
        break

      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,

    f.close()
  else:
    print 'Error downloading file'
