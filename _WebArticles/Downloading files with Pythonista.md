# Downloading files with Pythonista

_Captured: 2015-11-30 at 19:07 from [www.devwithimagination.com](http://www.devwithimagination.com/2014/05/06/downloading-files-with-pythonista/)_

![Pythonista Logo](http://www.devwithimagination.com/images/pythonista_ipad-p.png)

> _Pythonista Icon_

I have been trying to broaden the programming languages that I am familiar with and I am giving Python a shot. I have been trying out [Pythonista](http://omz-software.com/pythonista/) as my IDE. Pythonista is a universal app for iPad & iPhone ([iTunes link](https://itunes.apple.com/gb/app/pythonista/id528579881?mt=8&uo=4&at=10lsY7)). This is working out quite well for me, as it means I can read a book on my iPad, then just change apps to try out the things I have learned without needing to sit in front of my computer. It also allows me to do some more powerful things with my iOS devices.

The first script I want to share solves a little problem I have. While browsing the internet during the day on my iPhone, when I am away from my main computer, there will be files that I want to download later. Up to now the process has been to add a reminder with the link to come back to it later.

Now I can use Pythonista to download the file and upload it to my Dropbox folder. Later on, when I am at home, this will sync to my desktop and Hazel can process it appropriately.

## Why Pythonista?

Pythonista is by the same developer as [Editorial](https://itunes.apple.com/gb/app/editorial/id673907758?mt=8&uo=4&at=10lsY7), my iPad text editor [of choice](http://www.devwithimagination.com/2013/10/03/editorial-first-impressions-and-a-workflow/). The workflow system in Editorial is powered by the same Python backend, so the modules available in the two applications are mostly the same. This means that any scripts I develop in Pythonista can be used as part of a text workflow. Eventually I would like to integrate the [PyGitHub library](https://omz-forums.appspot.com/pythonista/post/4550380411158528) into something so I can commit updates to this site without needing my desktop, but I appreciate this is not going to be an easy task.

One of the annoyances I have had with this application is there is not an easy way to transport scripts between the two platforms. The current solutions appear to revolve around using the GitHub Gist service. An example, which I could not get to work, is called [gist check](https://gist.github.com/spencerogden/4702275).

I am working on a solution to this problem that will use the Dropbox API to sync files. I am currently testing this, but it seems to still have a few bugs that need ironed out before it is released to the wild.

If you are looking for a complete review of the application, this is not the place. I would suggest you check out Federico Viticci's excellent article: [Automating iOS: How Pythonista Changed My Workflow](http://www.macstories.net/stories/automating-ios-how-pythonista-changed-my-workflow/).

## Setting Up a Dropbox Developer Account

In order to use the Dropbox API you will require your own developer account. You will need to [create an app](https://www.dropbox.com/developers/apps) and plug in your own `APP_KEY` and `APP_SECRET` values into the script below. I set up my script to use a seperate application directory, but you can choose to use the root of your Dropbox by changing the `ACCESS_TYPE` variable.
    
    
    #### App folder
    
    A dedicated folder named after your app is created within the Apps folder of a user's Dropbox. Your app gets read and write access to this folder only and users can provide content to your app by moving files into this folder. Your app can also read and write datastores using the Datastore API.
    
    #### Full Dropbox
    
    You get full access to all the files and folders in a user's Dropbox, as well as permission to read and write datastores using the Datastore API.
    
    Your app should use the least privileged permission it can. When applying for production, we'll review that your app doesn't request an unnecessarily broad permission.
    

## The Script

This script takes in a single argument, the URL to download. This script is not complicated, and really should perform validation, but I am new to Python and still learning.

You can either set this argument by holding the Run button in Pythonista, which will display a "Run With Arguments" dialog, or by use of a bookmarklet. In Chrome I have a bookmarklet that will take the current page URL and call the script via the `pythonista://` URL scheme.

`javascript:window.location='pythonista://FileDownloader.py?action=run&argv='+ encodeURIComponent(location.href)`

The first time the script is run it will ask to be authenticated with Dropbox.
    
    
      1 # Script for downloading a URL to Dropbox
      2 import sys
      3 import urllib2
      4 import urllib
      5 import dropbox
      6 import os
      7 import console
      8 
      9 # Configuration
     10 DOWNLOAD_FOLDER = 'downloads'
     11 # Get your app key and secret from the Dropbox developer website
     12 APP_KEY = '<your app key>'
     13 APP_SECRET = '<your app secret>'
     14 # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
     15 ACCESS_TYPE = 'app_folder'
     16 
     17 ### Main program below ###
     18 PYTHONISTA_DOC_DIR = os.path.expanduser('~/Documents')
     19 SYNC_STATE_FOLDER = os.path.join(PYTHONISTA_DOC_DIR, 'dropbox_sync')
     20 TOKEN_FILEPATH = os.path.join(SYNC_STATE_FOLDER, TOKEN_FILENAME)
     21  
     22 def transfer_file(a_url):
     23 
     24     # Configure Dropbox
     25     sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
     26     configure_token(sess)
     27     client = dropbox.client.DropboxClient(sess)
     28     
     29     print "Attempting to download %s" % a_url
     30     
     31     file_name = a_url.split('/')[-1]
     32     file_name = urllib.unquote(file_name).decode('utf8') 
     33 
     34     
     35     if not os.path.exists(DOWNLOAD_FOLDER):
     36         os.makedirs(DOWNLOAD_FOLDER)
     37         
     38     download_file = os.path.join(DOWNLOAD_FOLDER, file_name)
     39     
     40     u = urllib2.urlopen(a_url)
     41     f = open(download_file, 'wb')
     42     meta = u.info()
     43     file_size = int(meta.getheaders("Content-Length")[0])
     44     print "Downloading: %s Bytes: %s" % (file_name, file_size)
     45     
     46     file_size_dl = 0
     47     block_sz = 8192
     48     while True:
     49         buffer = u.read(block_sz)
     50         if not buffer:
     51             break
     52 
     53         file_size_dl += len(buffer)
     54         f.write(buffer)
     55         status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
     56         status = status + chr(8)*(len(status)+1)
     57         print status,
     58         
     59     f.close()
     60     
     61     print "Uploading to dropbox"
     62     upload(download_file, client)
     63     
     64     # Delete the local file
     65     os.remove(download_file)
     66     
     67     print "DONE !"
     68 
     69 def upload(file, client):
     70     print "Trying to upload %s" % file
     71 
     72     response = client.put_file(file, open(file, 'r'), True)
     73     
     74     print "File %s uploaded to Dropbox" % file
     75     
     76  
     77 def configure_token(dropbox_session):
     78     if os.path.exists(TOKEN_FILEPATH):
     79         token_file = open(TOKEN_FILEPATH)
     80         token_key, token_secret = token_file.read().split('|')
     81         token_file.close()
     82         dropbox_session.set_token(token_key,token_secret)
     83     else:
     84         setup_new_auth_token(dropbox_session)
     85     pass
     86 
     87 def setup_new_auth_token(sess):
     88     request_token = sess.obtain_request_token()
     89     url = sess.build_authorize_url(request_token)
     90     
     91     # Make the user sign in and authorize this token
     92     print "url:", url
     93     print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
     94     webbrowser.open(url)
     95     raw_input()
     96     # This will fail if the user didn't visit the above URL and hit 'Allow'
     97     access_token = sess.obtain_access_token(request_token)
     98     #save token file
     99     token_file = open(TOKEN_FILEPATH,'w')
    100     token_file.write("%s|%s" % (access_token.key,access_token.secret) )
    101     token_file.close()
    102     pass
    103 
    104 def main():
    105 
    106     # Attempt to take a URL from the arguments
    107     the_url = None
    108     try:
    109         the_url = sys.argv[1]
    110     except IndexError:
    111         # no arguments, use the clipboard contents
    112         the_url = clipboard.get()
    113 
    114     if not the_url:
    115         print repr(sys.argv)
    116         return
    117 
    118     console.clear()
    119     transfer_file(the_url)
    120  
    121 if __name__ == '__main__':
    122     main()

This script is also available as a [gist](https://gist.github.com/dhutchison/113f634a034c13716925).

I would appriciate any feedback, as my coding experience these days is mostly Java and there may be a better way to do this in Python that I have missed.

## Next?

After my last few Python projects are complete, I think the next language I want to try my hand at will be JavaScript. I did my final year project at University in JavaScript and have barely touched it since. I have a handful of projects in mind that shouldn't be too difficult to achieve, but will still give me a good understanding of the language.
