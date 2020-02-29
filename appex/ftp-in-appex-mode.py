# coding: utf-8

# https://forum.omz-software.com/topic/3086/ftp-in-appex-mode/11

from __future__ import print_function
import console
from ftplib import FTP

user = 'Christian'
pwd = 'Xxxxxxx'
ftpok = True
try:
    ftp = FTP('iMac.local') #connect
    ftp.login(user,pwd)
except:
    ftpok = False
    console.alert('Mac not accessible','','Ok') 

if ftpok:
    console.alert('Mac accessible','','Ok') 
    source='Google Drive/Livres/Romans/'

    # Get all authors sub-dirctories
    authors = ftp.nlst(source)
    print(authors[0])
    ftp.quit()

