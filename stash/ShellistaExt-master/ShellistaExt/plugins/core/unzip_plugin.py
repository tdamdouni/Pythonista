'''unzip:
unzips a file
usage: unzip file [destination]
'''

from .. tools.toolbox import bash,pprint
import zipfile,os

def main(self, line):
    """unzip a zip archive"""
    # filename with optional destination
    args = bash(line)
    if args is None:
      return
    elif not (1 <= len(args) <= 2):
      print "unzip: Usage: unzip file [destination]"
    else:
      filename = os.path.abspath(args[0])
      if not os.path.isfile(filename):
        print "unzip: %s: No such file" % args[0]
      else:
        # PK magic marker check
        f = open(filename)
        try:
          pk_check = f.read(2)
        except Exception:
          pk_check = ''
        finally:
          f.close()
        if pk_check != 'PK':
          print "unzip: %s: does not appear to be a zip file" % args[0]
        else:
          if (os.path.basename(filename).lower().endswith('.zip')):
            altpath = os.path.splitext(os.path.basename(filename))[0]
          else:
            altpath = os.path.basename(filename) + '_unzipped'
          altpath = os.path.join(os.path.dirname(filename), altpath)
          location = (args[1:2] or [altpath])[0]
          if (os.path.exists(location)) and not (os.path.isdir(location)):
            print "unzip: %s: destination is not a directory" % location
            return
          elif not os.path.exists(location):
            os.makedirs(location)
          zipfp = open(filename, 'rb')
          try:
            zipf = zipfile.ZipFile(zipfp)
            # check for a leading directory common to all files and remove it
            dirnames = [os.path.join(os.path.dirname(x), '') for x in zipf.namelist()]
            common_dir = os.path.commonprefix(dirnames or ['/'])
            # Check to make sure there aren't 2 or more sub directories with the same prefix
            if not common_dir.endswith('/'):
              common_dir = os.path.join(os.path.dirname(common_dir), '')
            for name in zipf.namelist():
              data = zipf.read(name)
              fn = name
              if common_dir:
                if fn.startswith(common_dir):
                  fn = fn.split(common_dir, 1)[-1]
                elif fn.startswith('/' + common_dir):
                  fn = fn.split('/' + common_dir, 1)[-1]
              fn = fn.lstrip('/')
              fn = os.path.join(location, fn)
              dirf = os.path.dirname(fn)
              if not os.path.exists(dirf):
                os.makedirs(dirf)
              if fn.endswith('/'):
                # A directory
                if not os.path.exists(fn):
                  os.makedirs(fn)
              else:
                fp = open(fn, 'wb')
                try:
                  fp.write(data)
                finally:
                  fp.close()
          except Exception:
            zipfp.close()
            print "unzip: %s: zip file is corrupt" % args[0]
            return
          finally:
            zipfp.close()
