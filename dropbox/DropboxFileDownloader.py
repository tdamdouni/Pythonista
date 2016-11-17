# Script for downloading a URL to Dropbox
import sys
import urllib2
import urllib
import dropbox
import os
import console

# Configuration
TOKEN_FILENAME = 'PythonistaDropbox.token'
DOWNLOAD_FOLDER = 'downloads'
# Get your app key and secret from the Dropbox developer website
APP_KEY = 'XXXXXXXXXXX'
APP_SECRET = 'XXXXXXXXX'
# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

### Main program below ###
PYTHONISTA_DOC_DIR = os.path.expanduser('~/Documents')
SYNC_STATE_FOLDER = os.path.join(PYTHONISTA_DOC_DIR, 'dropbox_sync')
TOKEN_FILEPATH = os.path.join(SYNC_STATE_FOLDER, TOKEN_FILENAME)
 
def transfer_file(a_url):

    # Configure Dropbox
    sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    configure_token(sess)
    client = dropbox.client.DropboxClient(sess)
    
    print "Attempting to download %s" % a_url
    
    file_name = a_url.split('/')[-1]
    file_name = urllib.unquote(file_name).decode('utf8') 

    
    if not os.path.exists(DOWNLOAD_FOLDER):
    	os.makedirs(DOWNLOAD_FOLDER)
    	
    download_file = os.path.join(DOWNLOAD_FOLDER, file_name)
    
    u = urllib2.urlopen(a_url)
    f = open(download_file, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
        
    f.close()
    
    print "Uploading to dropbox"
    upload(download_file, client)
    
    # Delete the local file
    os.remove(download_file)
    
    print "DONE !"

def upload(file, client):
    print "Trying to upload %s" % file

    response = client.put_file(file, open(file, 'r'), True)
    
    print "File %s uploaded to Dropbox" % file
    
 
def configure_token(dropbox_session):
    if os.path.exists(TOKEN_FILEPATH):
        token_file = open(TOKEN_FILEPATH)
        token_key, token_secret = token_file.read().split('|')
        token_file.close()
        dropbox_session.set_token(token_key,token_secret)
    else:
        setup_new_auth_token(dropbox_session)
    pass

def setup_new_auth_token(sess):
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    
    # Make the user sign in and authorize this token
    print "url:", url
    print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
    webbrowser.open(url)
    raw_input()
    # This will fail if the user didn't visit the above URL and hit 'Allow'
    access_token = sess.obtain_access_token(request_token)
    #save token file
    token_file = open(TOKEN_FILEPATH,'w')
    token_file.write("%s|%s" % (access_token.key,access_token.secret) )
    token_file.close()
    pass

def main():

    # Attempt to take a URL from the arguments
    the_url = None
    try:
        the_url = sys.argv[1]
    except IndexError:
        # no arguments, use the clipboard contents
        the_url = clipboard.get()

    if not the_url:
        print repr(sys.argv)
        return

    console.clear()
    transfer_file(the_url)
 
if __name__ == '__main__':
    main()
