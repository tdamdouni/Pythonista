# https://github.com/geekcomputers/Pythonista/blob/master/update_jarvis.py

# http://www.thegeekblog.co.uk/the-geek-blog/2016/7/13/how-i-get-my-sqlite-database-onto-my-ios-devices-using-pythonista

# Script Name	: update_jarvis.py
# Author		: Craig Richards
# Created		: 01st July 2016
# Last Modified	: 
# Version		: 1.0

# Modifications	:

# Description	: Gets the latest copy of my SQLite database to the iOS devices

import dropbox
from dropboxlogin import get_client
import webbrowser

dropbox_client = get_client()
download=dropbox_client.get_file_and_metadata('/Databases/jarvis.db')
out=open('Jarvis/jarvis.db','wb')
download,metadata=dropbox_client.get_file_and_metadata('/Databases/jarvis.db')
out.write(download.read())
out.close()
webbrowser.open("workflow://")
