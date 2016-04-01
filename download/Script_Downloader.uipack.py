# coding: utf-8

# https://github.com/HeyItsJono/Pythonista

###############################################################################
# This is a self-extracting UI application package for Script_Downloader.
# Run this script once to extract the packaged application.
# The files will be extracted to Script_Downloader.py and Script_Downloader.pyui.
# Make sure that these files do not exist yet.
# To update from an older version, move or delete the old files first.
# After extracting, the application can be found at Script_Downloader.py.
# This bundle can be deleted after extraction.
###############################################################################
# Packaged using PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
###############################################################################

import console, os.path

NAME     = "Script_Downloader"
PYFILE   = """# coding: utf-8

import ui
import urllib2
import clipboard
from console import hud_alert
import console
import sys
import os

def parse_name(url):
	n = len(url)-1
	name = ''
	try:
		assert r'/' in url
	except AssertionError:
		return url
	for char in url:
		if url[n] != r'/':
			name = url[n] + name
			n += -1
		else:
			break
	return name

def parse_extension(name):
	n = len(name)-1
	extension = ''
	try:
		assert r'.' in name
	except AssertionError:
		return extension
	for char in name:
		if name[n] != r'.':
			extension = name[n] + extension
			n += -1
		else:
			break
	return extension
	

def download_tapped(sender):
	'@type sender: ui.Button'
	
	console.clear()

	urlfield = sender.superview['urlfield']
	filenamefield = sender.superview['filenamefield']
	extensionfield = sender.superview['extensionfield']
	extensioncontrol = sender.superview['extensioncontrol']

	if extensioncontrol.selected_index == 0:
		extension = '.py'
	elif extensioncontrol.selected_index == 1:
		extension = '.pyui'
	elif extensioncontrol.selected_index == 2:
		if extensionfield.text != '':
			if not '.' in extensionfield.text:
				extension = '.' + extensionfield.text
			else:
				extension = extensionfield.text
		else:
			extension = ''

	filename = filenamefield.text + extension
	filenum = 1
	while os.path.isfile(filename) is True:
		filename = filenamefield.text + ' ({})'.format(str(filenum)) + extension
		filenum += 1
	hud_alert('Downloading...')
	try:
		console.show_activity()
		url = urllib2.urlopen(urlfield.text).read()
	except (ValueError, urllib2.URLError):
		hud_alert('URL not valid', icon = 'error')
		sys.exit()
	hud_alert("Saving...")
	try:
		with open(filename, "w") as out_file:
			out_file.write(url)
			out_file.close()
	except IOError:
		os.makedirs(os.path.dirname(filename))
		with open(filename, "w") as out_file:
			out_file.write(url)
			out_file.close()
	console.hide_activity()
	hud_alert("Saved!")


def paste_tapped(sender):
	'@type sender: ui.Button'

	urlfield = sender.superview['urlfield']
	filenamefield = sender.superview['filenamefield']
	extensionfield = sender.superview['extensionfield']
	extensioncontrol = sender.superview['extensioncontrol']

	urlfield.text = unicode(clipboard.get())
	name = parse_name(urlfield.text)
	extension = parse_extension(name)
	name = name[:(len(name) - (len(extension) + 1))]
	filenamefield.text = name
	if extension == 'py':
		extensioncontrol.selected_index = 0
		extensionfield.text = ''
	elif extension == 'pyui':
		extensioncontrol.selected_index = 1
		extensionfield.text = ''
	else:
		extensioncontrol.selected_index = 2
		extensionfield.text = extension


def clear_tapped(sender):
	'@type sender: ui.Button'

	urlfield = sender.superview['urlfield']
	filenamefield = sender.superview['filenamefield']
	extensionfield = sender.superview['extensionfield']

	if sender.name == 'clearurl':
		urlfield.text = ''
	elif sender.name == 'clearname':
		filenamefield.text = ''
	elif sender.name == 'clearextension':
		extensionfield.text = ''


v = ui.load_view('Script_Downloader')
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present(orientations=['portrait'])
"""
PYUIFILE = """[{"class":"View","attributes":{"name":"Script Downloader","background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","tint_color":"RGBA(0.336735,0.663623,0.785714,1.000000)","enabled":true,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","flex":""},"frame":"{{0, 0}, {541, 377}}","nodes":[{"class":"TextField","attributes":{"alignment":"center","autocorrection_type":"no","font_size":17,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","enabled":true,"flex":"","placeholder":"Paste Raw URL Here","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","secure":false,"name":"urlfield","border_style":3,"uuid":"5360AD96-456E-4A90-83AE-BB1A6A3E908A","spellchecking_type":"no"},"frame":"{{6, 6}, {434, 83.5}}","nodes":[]},{"class":"SegmentedControl","attributes":{"name":"extensioncontrol","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","uuid":"4612E98D-1847-4E28-83AD-60C4938A08BF","enabled":true,"segments":".py|.pyui|Other","flex":"LR"},"frame":"{{7, 189}, {264, 83.5}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.928571,0.928571,0.928571,1.000000)","border_color":"RGBA(0.862245,0.897359,0.928571,1.000000)","font_size":15,"title":"Download","enabled":true,"flex":"","action":"download_tapped","font_bold":false,"name":"Downloadbutton","border_width":1,"uuid":"E21C39A0-F201-412C-A8A2-64EE8A5776F6","corner_radius":1},"frame":"{{7, 280.5}, {528, 88.5}}","nodes":[]},{"class":"TextField","attributes":{"alignment":"center","autocorrection_type":"no","font_size":17,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","enabled":true,"flex":"","placeholder":"Enter filename sans extension (Path optional)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","secure":false,"name":"filenamefield","border_style":3,"uuid":"930ECD80-962E-4E57-BD9B-C8B994516A88","spellchecking_type":"no"},"frame":"{{7, 97.5}, {528, 83.5}}","nodes":[]},{"class":"TextField","attributes":{"alignment":"center","autocorrection_type":"no","font_size":17,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","enabled":true,"flex":"","placeholder":"\\"Other\\" file extension","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","name":"extensionfield","border_style":3,"spellchecking_type":"no","uuid":"D3AABF4D-D6E2-4F9B-B75A-A285635B56ED"},"frame":"{{279, 189}, {256, 83.5}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.928571,0.928571,0.928571,1.000000)","image_name":"ionicons-clipboard-32","border_color":"RGBA(0.862245,0.898061,0.928571,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","action":"paste_tapped","font_bold":false,"name":"clipboard","border_width":1,"uuid":"135B3DD8-0A64-44F7-A818-86F79D9D5ACA","corner_radius":1},"frame":"{{448, 6}, {86, 83.5}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","image_name":"ionicons-ios7-close-24","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","tint_color":"RGBA(0.428571,0.428571,0.428571,1.000000)","action":"clear_tapped","font_bold":false,"alpha":0.5000000000000001,"name":"clearurl","uuid":"971A849B-E460-4E09-A049-5BBDE73FD5E6"},"frame":"{{406, 32}, {33, 30}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","image_name":"ionicons-ios7-close-24","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","tint_color":"RGBA(0.428571,0.428571,0.428571,1.000000)","action":"clear_tapped","font_bold":false,"alpha":0.5000000000000001,"name":"clearname","uuid":"5FF007B4-4F6B-4613-B801-9E654177E401"},"frame":"{{500.5, 122}, {33.5, 33}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","image_name":"ionicons-ios7-close-24","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","tint_color":"RGBA(0.428571,0.428571,0.428571,1.000000)","action":"clear_tapped","font_bold":false,"alpha":0.5000000000000001,"name":"clearextension","uuid":"DCA9375E-1982-48BC-B466-151C38720FEC"},"frame":"{{500, 214}, {33.5, 32.5}}","nodes":[]}]}]"""

def fix_quotes_out(s):
    return s.replace("\\\"\\\"\\\"", "\"\"\"").replace("\\\\", "\\")

def main():
    if os.path.exists(NAME + ".py"):
        console.alert("Failed to Extract", NAME + ".py already exists.")
        return
    
    if os.path.exists(NAME + ".pyui"):
        console.alert("Failed to Extract", NAME + ".pyui already exists.")
        return
    
    with open(NAME + ".py", "w") as f:
        f.write(fix_quotes_out(PYFILE))
    
    with open(NAME + ".pyui", "w") as f:
        f.write(fix_quotes_out(PYUIFILE))
    
    msg = NAME + ".py and " + NAME + ".pyui were successfully extracted!"
    console.alert("Extraction Successful", msg, "OK", hide_cancel_button=True)
    
if __name__ == "__main__":
    main()