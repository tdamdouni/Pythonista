'''gzip:
tar and gzip a file/directory
'''
from .. tools.toolbox import bash,pprint
import tarfile,os,io



def make_tarfile(source_dir):

    bytes = io.BytesIO()
    path = os.path.abspath(os.path.join(os.getcwd(),source_dir))
    with tarfile.open(fileobj = bytes, mode="w:gz") as tar:
      tar.add(path,arcname=os.path.basename(source_dir))
    tar.close()
    return bytes.getvalue()


def main(self, line):
  args = bash(line)
  if args == None:
    return
  elif len(args) == 1:
    path = os.getcwd() +'/'+ args[0]
  
    if os.path.isdir(path):
      name = args[0] + '.tar.gz'
    else:
      name = os.path.splitext(args[0])[0]+'.tar.gz'
    try :
      tar = make_tarfile(path)
      f = open(name,'wb')
      f.write(tar)
      f.close()
      print name + ' created.'
    except :
      print 'gzip: Cannot gzip file.'
  
  else:
    print 'gzip: too many parameters'
