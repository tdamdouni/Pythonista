# coding: utf-8
from youtube_dl import YoutubeDL
import webbrowser
import sys
import console

ydl = YoutubeDL({'quiet':True})

info = ydl.extract_info(sys.argv[1], download=False)

choice = console.alert('Download or Watch in Safari ','','Download','Watch')
if choice==1:
    webbrowser.open('r'+info['url'])
elif choice==2:
    webbrowser.open('safari-'+info['url'])
