'''untar:
untars an archive
usage: untar file [destination]
'''

from .. tools.toolbox import bash
import os,tarfile,shutil

def main(self, line):
    """untar a tar archive"""
    # filename with optional destination
    args = bash(line)
    if args is None:
      return
    elif not (1 <= len(args) <= 2):
      print "untar: Usage: untar file [destination]"
    else:
      filename = os.path.abspath(args[0])
      if not os.path.isfile(filename):
        print "untar: %s: No such file" % args[0]
      else:
        # 'ustar' magic marker check
        f = open(filename)
        try:
          f.seek(257)
          ustar_check = f.read(5)
        except Exception:
          ustar_check = ''
        finally:
          f.close()
        if ustar_check != 'ustar':
          print "untar: %s: does not appear to be a tar file" % args[0]
        else:
          if (os.path.basename(filename).lower().endswith('.tar')):
            altpath = os.path.splitext(os.path.basename(filename))[0]
          else:
            altpath = os.path.basename(filename) + '_untarred'
          altpath = os.path.join(os.path.dirname(filename), altpath)
          location = (args[1:2] or [altpath])[0]
          if (os.path.exists(location)) and not (os.path.isdir(location)):
            print "untar: %s: destination is not a directory" % location
            return
          elif not os.path.exists(location):
            os.makedirs(location)
          try:
            tar = tarfile.open(filename, 'r')
            # check for a leading directory common to all files and remove it
            dirnames = [os.path.join(os.path.dirname(x.name), '') for x in tar.getmembers() if x.name != 'pax_global_header']
            common_dir = os.path.commonprefix(dirnames or ['/'])
            if not common_dir.endswith('/'):
              common_dir = os.path.join(os.path.dirname(common_dir), '')
            for member in tar.getmembers():
              fn = member.name
              if fn == 'pax_global_header':
                continue
              if common_dir:
                if fn.startswith(common_dir):
                  fn = fn.split(common_dir, 1)[-1]
                elif fn.startswith('/' + common_dir):
                  fn = fn.split('/' + common_dir, 1)[-1]
              fn = fn.lstrip('/')
              fn = os.path.join(location, fn)
              dirf = os.path.dirname(fn)
              if member.isdir():
                # A directory
                if not os.path.exists(fn):
                  os.makedirs(fn)
              elif member.issym():
                # skip symlinks
                continue
              else:
                try:
                  fp = tar.extractfile(member)
                except (KeyError, AttributeError):
                  # invalid member, not necessarily a bad tar file
                  continue
                if not os.path.exists(dirf):
                  os.makedirs(dirf)
                with open(fn, 'wb') as destfp:
                  shutil.copyfileobj(fp, destfp)
                fp.close()
          except Exception, e:
            print e
            tar.close()
            print "untar: %s: tar file is corrupt" % args[0]
            return
          finally:
            tar.close()
