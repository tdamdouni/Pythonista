#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
__author__ = "Claus Haslauer (mail@planetwater.org)"
__version__ = "Revision: 0.1 $"
__date__ = "Date: 2014/01/05 $"
__copyright__ = "Copyright (c) 2014 Claus Haslauer"
__license__ = "CC BY-NC 3.0"

import os
import sys
import requests
import datetime
import dropbox
import console
import webbrowser

## DROPBOX STUFF ---------------------------------------------------------------
TOKEN_FILENAME = 'Pythonista_2.token'
APP_KEY = 'STRING1'
APP_SECRET = 'STRING2'
# # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'

## NEWSPAPER STUFF -------------------------------------------------------------
base_url = 'http://download_URL/'
usr_name = 'usr'
pw ='pw'

## DROPBOX related functions ---------------------------------------------------
def configure_token(dropbox_session):
    if os.path.exists(TOKEN_FILENAME):
        token_file = open(TOKEN_FILENAME)
        token_key, token_secret = token_file.read().split('|')
        token_file.close()
        dropbox_session.set_token(token_key,token_secret)
    else:
        first_access(dropbox_session)
    pass
 
def first_access(sess):
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    
    # Make the user sign in and authorize this token
    print("url:", url)
    print("Please visit this website and press the 'Allow' button, then hit 'Enter' here.")
    webbrowser.open(url)
    raw_input()
    # This will fail if the user didn't visit the above URL and hit 'Allow'
    access_token = sess.obtain_access_token(request_token)
    #save token file
    token_file = open(TOKEN_FILENAME,'w')
    token_file.write("%s|%s" % (access_token.key,access_token.secret) )
    token_file.close()
    pass


def main():
    """
    sys arg: give one integer!
             0 ... today
            +1 ... tomorrow

    some more description here:
        http://planetwater.org/2014/01/09/fun-with-python-script-for-daily-newspaper/
    """
    # start with a clear console
    console.clear()
    
    delta_day = int(sys.argv[1])
    print('delta_day: ', delta_day)
    
    # dropbox initialization
    sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    configure_token(sess)
    client = dropbox.client.DropboxClient(sess)
    print("linked account: %s" % client.account_info()['display_name'])
    
    # get today's date (for pdf file name)
    today = datetime.datetime.utcnow()
    target_date = today + datetime.timedelta(days=delta_day)
    filename = target_date.strftime("%Y_%m_%d.pdf")

    ## check if the file I am about to download might already exist on dropbox
    drb_path = '/Apps/Pythonista/'
    exists = client.search(drb_path, filename)
    if len(exists) > 0:
        print('file already exists on dropbox!')
        raise Exception
    
    ## stick url together
    url = base_url + today_string + '.pdf'
    print(url)
    r = requests.get(url, auth=(usr_name, pw))
    
    ## if something is wrong with download status
    if r.status_code != 200:
        print('ERROR!')
        print('likely, you chose a wrong date!')
        raise Exception
    
    print('\n')
    print(r)
    
    ## saving pdf file locally
    # not sure which value is good. 32 seems like it worked
    chunk_size = 32
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print('file saved in pythonista')
    
    # save file to dropbox
    f = open(filename)
    response = client.put_file(drb_path + filename, f)
    print("uploaded to dropbox \n:", response)
    
    # get dropbox url which is then used to open pdf in goodreader
    share_url = client.media('/Apps/Pythonista/' + filename)
    url =share_url.get('url', 'not found')
    
    # open in goodreader
    webbrowser.open('g'+url)
    
    # delete local file in pythonista
    os.remove(filename)
    print('\n file removed from pythonista')
    
    print("Done!")
    
    
if __name__ == '__main__':
    main()