# coding: utf-8

# https://forum.omz-software.com/topic/2532/python-spirographs-anyone

'''This script will copy 7 python files locally and then open a webpage...'''

import console, requests, webbrowser

file_names = 'Spirograph SpirographDriver WindowsBMP LineDrawer ColourMap CircleDrawer MakeFileList'
url_root = 'http://www.eddaardvark.co.uk/python_patterns/code/'
fmt = 'Creating local file {}: {}'

for i, file_name in enumerate(''.split()):
    file_name += '.py'
    text = requests.get(url_root + file_name).text
    if text:
        console.hud_alert(fmt.format(i+1, file_name))
        with open(file_name, 'w') as out_file:
            out_file.write(text)

url_root = url_root.rsplit('/', 2)[0]
webbrowser.open(url_root)
#webbrowser.open(url_root + '/spirograph.html')
