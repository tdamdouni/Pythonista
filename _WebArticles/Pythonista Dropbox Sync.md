# Pythonista Dropbox Sync

_Captured: 2015-09-28 at 22:43 from [www.devwithimagination.com](http://www.devwithimagination.com/2014/05/11/pythonista-dropbox-sync/)_

![Pythonista Logo](http://www.devwithimagination.com/images/pythonista_ipad-p.png)

> _Pythonista Icon_

Continuing on from [my last post](http://dev-lamp.local/2014/05/06/downloading-files-with-pythonista/), I have been delving into Python using [Pythonista](https://itunes.apple.com/gb/app/pythonista/id528579881?mt=8&uo=4&at=10lsY7). Syncing scripts between platforms is not as simple as it could be, but now I have a solution. It is not perfect, but it does the job for me and it is developed in Python!

## NewFromGist.py

Before we get on to the main script, there is this script that is useful for importing scripts into the application that have been shared by others, assuming the script is available as a [Gist](https://gist.github.com/).

This is a fork of a [script](https://gist.github.com/omz/4076735) by the application author, Ole Zorn. I have only made a couple of modifications to it:

  1. Changed to handle the format of gist URLs that contain the author
  2. Added support for the URL of the Gist to be supplied via an argument.

I wanted the ability to supply an argument so I could launch this script as a bookmarklet in Chrome, which switches to Pythonista and downloads the new script.

My bookmarklet is just:

`javascript:window.location='pythonista://NewFromGist.py?action=run&argv='+ encodeURIComponent(location.href)`
    
    
      1 ### Based on: https://gist.github.com/b0644f5ed1d94bd32805
      2 ### This version strips unicode characters from the downloaded script
      3 ### to work around the currently limited unicode support of the editor
      4 ### module.
      5 
      6 # This script downloads and opens a Gist from a URL in the clipboard.
      7 # It's meant to be put in the editor's actions menu.
      8 #
      9 # It works with "raw" and "web" gist URLs, but not with gists that
     10 # contain multiple files or non-Python files.
     11 #
     12 # If a file already exists, a dialog is shown that asks whether the
     13 # new file should be renamed automatically.
     14 
     15 import clipboard
     16 import editor
     17 import console
     18 import re
     19 import os
     20 import sys
     21 
     22 class InvalidGistURLError (Exception): pass
     23 class MultipleFilesInGistError (Exception): pass
     24 class NoFilesInGistError (Exception): pass
     25 class GistDownloadError (Exception): pass
     26 
     27 def download_gist(gist_url):
     28   # Returns a 2-tuple of filename and content
     29   # console.show_activity()
     30   raw_match = re.match('http(s?)://raw.github.com/gist/', gist_url)
     31   if raw_match:
     32     import requests
     33     from urlparse import urlparse
     34     filename = os.path.split(urlparse(gist_url).path)[1]
     35     try:
     36       r = requests.get(gist_url)
     37       content = r.text
     38       return filename, content
     39     except:
     40       raise GistDownloadError()
     41   else:
     42     gist_id_match = re.match('http(s?)://gist.github.com/([0-9A-Za-z]*/){0,1}([0-9a-f]*)', gist_url)
     43     if gist_id_match:
     44       import requests
     45       gist_id = gist_id_match.group(3)
     46       json_url = 'https://api.github.com/gists/' + gist_id
     47       try:
     48         import json
     49         gist_json = requests.get(json_url).text
     50         gist_info = json.loads(gist_json)
     51         files = gist_info['files']
     52       except:
     53         raise GistDownloadError()
     54       py_files = []
     55       for file_info in files.values():
     56         lang =  file_info.get('language', None)
     57         if lang != 'Python':
     58           continue
     59         py_files.append(file_info)
     60       if len(py_files) > 1:
     61         raise MultipleFilesInGistError()
     62       elif len(py_files) == 0:
     63         raise NoFilesInGistError()
     64       else:
     65         file_info = py_files[0]
     66         filename = file_info['filename']
     67         content = file_info['content']
     68         return filename, content
     69     else:
     70       raise InvalidGistURLError()
     71 
     72 def main():
     73 
     74   try:
     75     gist_url = sys.argv[1]
     76   except IndexError:
     77     gist_url = clipboard.get()
     78 
     79   try:
     80     filename, content = download_gist(gist_url)
     81     content = content.encode('ascii', 'ignore')
     82     if os.path.isfile(filename):
     83       i = console.alert('File exists', 'A file with the name ' + filename +
     84                         ' already exists in your library.',
     85                         'Auto Rename')
     86       if i == 1:
     87         editor.make_new_file(filename, content)
     88     else:
     89       editor.make_new_file(filename, content)
     90   except InvalidGistURLError:
     91     console.alert('No Gist URL',
     92                   'The clipboard doesn\'t seem to contain a valid Gist URL.',
     93                   'OK')
     94   except MultipleFilesInGistError:
     95     console.alert('Multiple Files', 'This Gist contains multiple ' +
     96                   'Python files, which isn\'t currently supported.')
     97   except NoFilesInGistError:
     98     console.alert('No Python Files', 'This Gist contains no Python files.')
     99   except GistDownloadError:
    100     console.alert('Error', 'The Gist could not be downloaded.')
    101 
    102 if __name__ == '__main__':
    103   main()

This script is also [available as a gist](https://gist.github.com/dhutchison/8528503).

## DropboxSync.py

Now on to the script that I've spent quite a bit of time developing. I feel this has given me a reasonably complex problem to develop my knowledge of Python with.

As in my [previous post](http://dev-lamp.local/2014/05/06/downloading-files-with-pythonista/), this script requires a [Dropbox API key](https://www.dropbox.com/developers/apps). This will attempt to sync all the scripts in the Pythonista application with Dropbox. This performs two way sync, and keeps a state file to maintain what revision of a file is held locally.

This uses the Dropbox API in the way that should maintain versions of files, so you should be able to restore previous versions of scripts if needed.

**Standard disclaimer applies:** **_Make sure you have recent copies of any scripts, sync is hard. Bugs happen. This has been tested for my purposes, but there may be some edge cases that it does not handle._**

The latest version of this script is available [on github](https://github.com/dhutchison/PythonistaScripts/blob/master/DropboxSync.py).
    
    
      1 import webbrowser, os, pprint
      2 import dropbox
      3 import hashlib
      4 import json
      5 import difflib
      6 import sys
      7 
      8 # Configuration
      9 TOKEN_FILENAME = 'PythonistaDropbox.token'
     10 # Get your app key and secret from the Dropbox developer website
     11 APP_KEY = '<app key>'
     12 APP_SECRET = '<app secret>'
     13 
     14 # ACCESS_TYPE can be 'dropbox' or 'app_folder' as configured for your app
     15 ACCESS_TYPE = 'app_folder'
     16 
     17 # Program, do not edit from here
     18 VERBOSE_LOGGING = False
     19 
     20 PYTHONISTA_DOC_DIR = os.path.expanduser('~/Documents')
     21 SYNC_STATE_FOLDER = os.path.join(PYTHONISTA_DOC_DIR, 'dropbox_sync')
     22 TOKEN_FILEPATH = os.path.join(SYNC_STATE_FOLDER, TOKEN_FILENAME)
     23 
     24 pp = pprint.PrettyPrinter(indent=4)
     25 
     26 # Method to get the MD5 Hash of the file with the supplied file name.
     27 def getHash(file_name):
     28   # Open,close, read file and calculate MD5 on its contents
     29   with open(file_name) as file_to_check:
     30     # read contents of the file
     31     data = file_to_check.read()
     32     # pipe contents of the file through
     33     file_hash = hashlib.md5(data).hexdigest()
     34   return file_hash
     35 
     36 # Method to configure the supplied dropbox session.
     37 # This will use cached OAUTH credentials if they have been stored, otherwise the
     38 # user will be put through the Dropbox authentication process.
     39 def configure_token(dropbox_session):
     40   if os.path.exists(TOKEN_FILEPATH):
     41     token_file = open(TOKEN_FILEPATH)
     42     token_key, token_secret = token_file.read().split('|')
     43     token_file.close()
     44     dropbox_session.set_token(token_key,token_secret)
     45   else:
     46     setup_new_auth_token(dropbox_session)
     47   pass
     48 
     49 # Method to set up a new Dropbox OAUTH token.
     50 # This will take the user through the required steps to authenticate.
     51 def setup_new_auth_token(sess):
     52   request_token = sess.obtain_request_token()
     53   url = sess.build_authorize_url(request_token)
     54 
     55   # Make the user sign in and authorize this token
     56   print "url:", url
     57   print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
     58   webbrowser.open(url)
     59   raw_input()
     60   # This will fail if the user didn't visit the above URL and hit 'Allow'
     61   access_token = sess.obtain_access_token(request_token)
     62   #save token file
     63   token_file = open(TOKEN_FILEPATH,'w')
     64   token_file.write("%s|%s" % (access_token.key,access_token.secret) )
     65   token_file.close()
     66   pass
     67 
     68 def upload(file, details, client, parent_revision):
     69   print "Trying to upload %s" % file
     70   details['md5hash'] = getHash(file)
     71   print "New MD5 hash: %s" % details['md5hash']
     72 
     73   response = client.put_file(file, open(file, 'r'), False, parent_revision)
     74   #print "Response: %s" % response
     75   details = update_file_details(details, response)
     76 
     77   print "File %s uploaded to Dropbox" % file
     78 
     79   return details
     80 
     81 def download(dest_path, dropbox_metadata, details, client):
     82   out = open(dest_path, 'w')
     83   file_content = client.get_file(dropbox_metadata['path']).read()
     84   out.write(file_content)
     85 
     86   details['md5hash'] = getHash(dest_path)
     87   print "New MD5 hash: %s" % details['md5hash']
     88   details = update_file_details(details, dropbox_metadata)
     89 
     90   return details
     91 
     92 def process_folder(client, dropbox_dir, file_details):
     93 
     94   # Get the metadata for the directory being processed (dropbox_dir).
     95   # If the directory does not exist on Dropbox it will be created.
     96   try:
     97     folder_metadata = client.metadata(dropbox_dir)
     98 
     99     if VERBOSE_LOGGING == True:
    100       print "metadata"
    101       pp.pprint(folder_metadata)
    102   except dropbox.rest.ErrorResponse as error:
    103     pp.pprint(error.status)
    104     if error.status == 404:
    105       client.file_create_folder(dropbox_dir)
    106       folder_metadata = client.metadata(dropbox_dir)
    107     else:
    108       pp.pprint(error)
    109       raise error
    110 
    111   # If the directory does not exist locally, create it.
    112   local_folder = os.path.join(PYTHONISTA_DOC_DIR, dropbox_dir[1:])
    113   if not os.path.exists(local_folder):
    114     os.mkdir(local_folder)
    115 
    116 
    117   # All the files that have been processed so far in this folder.
    118   processed_files = []
    119   # All the directories that exist on Dropbox in the current folder that need to be processed.
    120   dropbox_dirs = []
    121   # All the local directories in this current folder that do not exist in Dropbox.
    122   local_dirs = []
    123 
    124   # Go through the files currently in Dropbox and compare with local
    125   for file in folder_metadata['contents']:
    126     dropbox_path = file['path'][1:]
    127     file_name = file['path'].split('/')[-1]
    128     if file['is_dir'] == False and file['mime_type'].endswith('python'):
    129 
    130       if not os.path.exists(os.path.join(PYTHONISTA_DOC_DIR, dropbox_path)):
    131         print "Processing Dropbox file %s (%s)" % (file['path'], dropbox_path)
    132         try:
    133 
    134 
    135           if dropbox_path in file_details:
    136             # in cache but file no longer locally exists
    137             details = file_details[dropbox_path]
    138 
    139             print "File %s is in the sync cache and on Dropbox, but no longer exists locally. [Delete From Dropbox (del)|Download File (d)] (Default Delete)" % file['path']
    140 
    141             choice = raw_input()
    142             if (choice == 'd'):
    143               download_file = True
    144             else:
    145               # Default is 'del'
    146               download_file = False
    147 
    148               #delete the dropbox copy
    149               client.file_delete(file['path'])
    150               file_details.remove(dropbox_path)
    151 
    152           else:
    153             details = {}
    154             download_file = True
    155 
    156           if (download_file ==  True):
    157             print "Downloading file %s (%s)" % (file['path'], dropbox_path)
    158             if VERBOSE_LOGGING == True:
    159               print details
    160 
    161             details = download(dropbox_path, file, details, client)
    162             file_details[dropbox_path] = details
    163 
    164           # dealt with this file, don't want to touch it again later
    165           processed_files.append(file_name)
    166           write_sync_state(file_details)
    167 
    168         except:
    169           pass
    170       else:
    171         # need to check if we should update this file
    172         # is this file in our map?
    173         if dropbox_path in file_details:
    174           details = file_details[dropbox_path]
    175 
    176           if VERBOSE_LOGGING == True:
    177             print "Held details are: %s" % details
    178 
    179           if details['revision'] == file['revision']:
    180             # same revision
    181             current_hash = getHash(dropbox_path)
    182 
    183             if VERBOSE_LOGGING == True:
    184               print 'New hash: %s, Old hash: %s' % (current_hash, details['md5hash'])
    185 
    186             if current_hash == details['md5hash']:
    187               print 'File "%s" not changed.' % dropbox_path
    188             else:
    189               print 'File "%s" updated locally, uploading...' % dropbox_path
    190 
    191               details = upload(dropbox_path, details, client, file['rev'])
    192               file_details[dropbox_path] = details
    193 
    194             processed_files.append(file_name)
    195           else:
    196             #different revision
    197             print 'Revision of "%s" changed from %s to %s. ' % (dropbox_path, details['revision'], file['revision'])
    198 
    199             current_hash = getHash(dropbox_path)
    200 
    201             if VERBOSE_LOGGING == True:
    202               print 'File %s. New hash: %s, Old hash: %s' % (dropbox_path, current_hash, details['md5hash'])
    203 
    204             if current_hash == details['md5hash']:
    205               print 'File "%s" updated remotely. Downloading...' % dropbox_path
    206 
    207               details = download(dropbox_path, file, details, client)
    208               file_details[dropbox_path] = details
    209             else:
    210               print "File %s has been updated both locally and on Dropbox. Overwrite [Dropbox Copy (d)|Local Copy (l)| Skip(n)] (Default Skip)" % file['path']
    211               choice = raw_input()
    212 
    213               if choice == 'd' or choice == 'D':
    214                 print "Overwriting Dropbox Copy of %s" % file
    215                 details = upload(dropbox_path, details, client, file['rev'])
    216                 file_details[dropbox_path] = details
    217               elif choice == 'l' or choice == 'L':
    218                 print "Overwriting Local Copy of %s" % file
    219                 details = download(dropbox_path, file, details, client)
    220                 file_details[dropbox_path] = details
    221 
    222 
    223         else:
    224           # Not in cache, but exists on dropbox and local, need to prompt user
    225 
    226           print "File %s is not in the sync cache but exists both locally and on dropbox. Overwrite [Dropbox Copy (d)|Local Copy (l) | Skip(n)] (Default Skip)" % file['path']
    227           choice = raw_input()
    228 
    229           details = {}
    230           if choice == 'd' or choice == 'D':
    231             print "Overwriting Dropbox Copy of %s" % file
    232             details = upload(dropbox_path, details, client, file['rev'])
    233             file_details[dropbox_path] = details
    234           elif choice == 'l' or choice == 'L':
    235             print "Overwriting Local Copy of %s" % file
    236             details = download(dropbox_path, file, details, client)
    237             file_details[dropbox_path] = details
    238           else:
    239             print "Skipping processing for file %s" % file
    240 
    241         # Finished dealing with this file, update the sync state and mark this file as processed.
    242         write_sync_state(file_details)
    243         processed_files.append(file_name)
    244     elif file['is_dir'] == True:
    245       dropbox_dirs.append(file['path'])
    246 
    247 
    248   # go through the files that are local but not on Dropbox, upload these.
    249   files = os.listdir(local_folder)
    250   for file in files:
    251 
    252     full_path = os.path.join(local_folder, file)
    253     relative_path = os.path.relpath(full_path)
    254     db_path = '/'+relative_path
    255 
    256     if not file in processed_files and not os.path.isdir(file) and not file.startswith('.') and file.endswith('.py'):
    257 
    258       if VERBOSE_LOGGING == True:
    259         print 'Searching "%s" for "%s"' % (dropbox_dir, file)
    260       found = client.search(dropbox_dir, file)
    261 
    262       if found:
    263         print "File found on Dropbox, this shouldn't happen! Skipping %s..." % file
    264       else:
    265         if VERBOSE_LOGGING == True:
    266           pp.pprint(file)
    267 
    268         if file in file_details:
    269           details = file_details[file]
    270         else:
    271           details = {}
    272         print details
    273 
    274         details = upload(relative_path, details, client, None )
    275         file_details[relative_path] = details
    276         write_sync_state(file_details)
    277 
    278     elif not db_path in dropbox_dirs and os.path.isdir(file) and not file.startswith('.') and not file == SYNC_STATE_FOLDER:
    279       local_dirs.append(db_path)
    280 
    281 
    282   #process the directories
    283   for folder in dropbox_dirs:
    284     if VERBOSE_LOGGING == True:
    285       print 'Processing dropbox dir %s from %s' % (folder, dropbox_dir)
    286     process_folder(client, folder, file_details)
    287 
    288   for folder in local_dirs:
    289     if VERBOSE_LOGGING == True:
    290       print 'Processing local dir %s from %s' % (folder, dropbox_dir)
    291     process_folder(client, folder, file_details)
    292 
    293 def update_file_details(file_details, dropbox_metadata):
    294   file_details['revision'] = dropbox_metadata['revision']
    295   file_details['rev'] = dropbox_metadata['rev']
    296   file_details['modified'] = dropbox_metadata['modified']
    297   file_details['path'] = dropbox_metadata['path']
    298   return file_details
    299 
    300 def write_sync_state(file_details):
    301   # Write sync state file
    302   sync_status_file = os.path.join(SYNC_STATE_FOLDER, 'file.cache.txt')
    303 
    304   if VERBOSE_LOGGING:
    305     print 'Writing sync state to %s' % sync_status_file
    306 
    307   with open(sync_status_file, 'w') as output_file:
    308     json.dump(file_details, output_file)
    309 
    310 def main():
    311 
    312   # Process any supplied arguments
    313   global VERBOSE_LOGGING
    314   for argument in sys.argv:
    315     if argument == '-v':
    316       VERBOSE_LOGGING = True
    317 
    318   # Load the current sync status file, if it exists.
    319   sync_status_file = os.path.join(SYNC_STATE_FOLDER, 'file.cache.txt')
    320 
    321   if not os.path.exists(SYNC_STATE_FOLDER):
    322     os.mkdir(SYNC_STATE_FOLDER)
    323   if os.path.exists(sync_status_file):
    324     with open(sync_status_file, 'r') as input_file:
    325       file_details = json.load(input_file)
    326   else:
    327     file_details = {}
    328 
    329   if VERBOSE_LOGGING == True:
    330     print "File Details: "
    331     pp.pprint(file_details)
    332 
    333   #configure dropbox
    334   sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    335   configure_token(sess)
    336   client = dropbox.client.DropboxClient(sess)
    337 
    338   print "linked account: %s" % client.account_info()['display_name']
    339   #pp.pprint (client.account_info())
    340 
    341   process_folder(client, '/', file_details)
    342 
    343   # Write sync state file
    344   write_sync_state(file_details)
    345 
    346 
    347 if __name__ == "__main__":
    348   print 'Begin Dropbox sync'
    349   main()
    350   print 'Dropbox sync done!'

Any feedback on either of these scripts is welcome. I'm just starting to learn Python and it is very different from any language I have tried in the past!
