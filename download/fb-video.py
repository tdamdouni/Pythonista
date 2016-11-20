# coding: utf-8

# https://forum.omz-software.com/topic/3626/play-video-on-ios-quick-look/5

import webbrowser, os, requests, re, bs4
import appex
import console
import dialogs

data_dir = os.path.join(os.path.abspath('.'),'Videos')

if not os.path.isdir (data_dir):
	#print(data_dir)
	os.makedirs(data_dir)
	
os.chdir(data_dir)
#ßprint(os.path.abspath('.'))


def DownloadFile(url, filename):
	res = requests.get(url)
	
	try:
		res.raise_for_status()
	except Exception as exc:
		print('There was a problem: %s' % (exc))
		
	with open(filename, "wb") as code:
		code.write(res.content)
		
# the URL below is copy from the console of the above script, I don't know why it quits without saving the file after download but it works in this script

url = 'https://video-hkg3-1.xx.fbcdn.net/v/t42.9040-2/10000000_1416830291949591_1471786757199495168_n.mp4?efg=eyJybHIiOjMzNjEsInJsYSI6NDA5NiwidmVuY29kZV90YWciOiJzdmVfaGQifQ%5Cu00253D%5Cu00253D&rl=3361&vabr=2241&oh=a820c423f12ecc6472d83bd9e9d8432b&oe=581ABB82'

DownloadFile(url, 'temp.mp4')
console.quicklook('temp.mp4')
os.remove('temp.mp4')
