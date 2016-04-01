# coding: utf-8

# https://github.com/mncfre/Save_Videos

# Save_Videos
# With this script you can download on your iOS devices videos from youtube, Facebook, instagram, and many more pages, using the Youtube-dl Library adapted to Pythonista by hyshai.
# Requiements:
# - Youtube-dl Library installed on your Pythonista: https://github.com/HyShai/youtube-dl
# - Workflow for iOS
# - Pythonista for iOS

# You need to import the workflows:
# - SaveTube: https://workflow.is/workflows/8affc84b602f486a83840d24bda238a7
# - DownTube: https://workflow.is/workflows/6b237fd76f5c49e8b0f1f3ad61c32d24

# Usage: Just send link via "Open In" to SaveTube or run SaveTube and paste the link to be downloaded.

from youtube_dl import YoutubeDL
import webbrowser
from urllib import quote_plus
import clipboard
from re import sub
import console
import unicodedata
import ui

def strip_accents(s):
	return ''.join(c for c in unicodedata.normalize('NFD', s)
	if unicodedata.category(c) != 'Mn')

def paste_tapped(sender):
	# Get the root view:
	v = sender.superview
	if webbrowser.can_open(clipboard.get()):
		v['urlfield'].text = clipboard.get()
	else: 
		console.hud_alert('Invalid URL')
	
@ui.in_background
def download(sender):
	# Get the root view:
	v = sender.superview
	link = v['urlfield'].text
	if sender.name == 'download':
		#Download Button Disabled
		sender.enabled = False
		console.show_activity('Downloading...')
		if v['qualityopt'].text== 'Low':
			ydl = YoutubeDL({'quiet':True,'format':'36/5/43/18/22'})
		elif v['qualityopt'].text== 'Medium':
			ydl = YoutubeDL({'quiet':True,'format':'18/135/43/134/133/160'})
		elif v['qualityopt'].text== 'Best':
			ydl = YoutubeDL({'quiet':True,'format':'best'})
		
		try:
			info = ydl.extract_info(link, download=False)
		except:
			try:
				console.show_activity('Trying with another video quality...')
				ydl = YoutubeDL({'quiet':True,'format':'best'})
				info = ydl.extract_info(link, download=False)
			except:
				console.hud_alert('Invalid URL')
				console.hide_activity()
				sender.enabled = True
				return 
			
		#print info['url']
	
		download_url = info['url']
		#print download_url
	
		titulo = info['title']
	
		#Codifico el titulo para URL
		#elimino ascentos
		titulo=strip_accents(titulo)
		#elimino simbolos
		titulo=sub(r'[^a-zA-Z0-9 ]','',titulo)
	
		try:
			titulo = quote_plus(titulo)
		except:
			console.show_activity('Impossible to encode title')
			titulo = 'Video_Downloaded'
		#print 'It will be downloaded: '+info['title']
		
		if v['audio'].value==False:
			audio = '0_'
		else: 
			audio = '1_'
		
		#Copio el link de descarga
		clipboard.set(download_url)
		console.hide_activity()
		if v['swexit'].value:
			v.close()
		#Download Button Enabled
		sender.enabled = True 
		webbrowser.open('workflow://run-workflow?name=DownTube&input='+audio+titulo)
		

def slider_action(sender):
	# Get the root view:
	v = sender.superview
	# Update Quality
	if sender.name == 'quality':
		if v['quality'].value <= 0.33:
			v['qualityopt'].text = 'Low'
		elif v['quality'].value > 0.33 and v['quality'].value <= 0.66:
			v['qualityopt'].text = 'Medium'
		elif v['quality'].value > 0.66:
			v['qualityopt'].text = 'Best'


v = ui.load_view('YoutubeNow2')
urlfield = v['urlfield']
if webbrowser.can_open(clipboard.get()):
	urlfield.text = clipboard.get()
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present(orientations=['portrait'])