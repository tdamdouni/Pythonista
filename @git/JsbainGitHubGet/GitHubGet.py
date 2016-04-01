# download an entire github repo.
#
# either copy the url to clipboard, and run script, or run following bookmarklet.  
# will unzip to repo-branch (so be careful if downloading same branch name from multiple users)
# 
##   javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://GitHubGet?action=run&argv='+document.location.href;%7D)();


import urllib,zipfile,sys, clipboard, functools, re, os, tempfile

def extract_git_id(git):
    print git
    m = re.match((r'^http(s?)://([\w-]*\.)?github\.com/(?P<user>[\w-]+)/(?P<repo>[\w-]*)'
                 '((/tree|/blob)/(?P<branch>[\w-]*))?'), git)
#    print m.groupdict()
    return m
    
def git_download_from_args(args):
    if len(args) == 2:
        url = args[1]
    else:
        url = clipboard.get()
    git_download(url)


def dlProgress(filename, count, blockSize, totalSize):
    if count*blockSize > totalSize:
        percent=100
    else:
        percent = max(min(int(count*blockSize*100/totalSize),100),0)
    sys.stdout.write("\r" + filename + "...%d%%" % percent)
    sys.stdout.flush()

def git_download(url):
    base='https://codeload.github.com'
    archive='zip'
    m=extract_git_id(url)
    if m:
        g=m.groupdict()
        if not g['branch']:
            g['branch']='master'

        u=   '/'.join((base,g['user'],g['repo'],archive, g['branch']))
        #print u
        try:
            with tempfile.NamedTemporaryFile(mode='w+b',suffix='.zip') as f:
                urllib.urlretrieve(u,f.name,reporthook=functools.partial(dlProgress,u))
                z=zipfile.ZipFile(f)
                z.extractall()
                print z.namelist()
        except:
            print('git url did not return zip file')
    else:
        print('could not determine repo url from clipboard or argv')
        
if __name__=='__main__':
    git_download_from_args(sys.argv)
