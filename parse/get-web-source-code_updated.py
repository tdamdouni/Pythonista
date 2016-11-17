# coding: utf-8

# https://forum.omz-software.com/topic/2582/get-web-source-code/7

import appex
import requests
import os
import ui
import console
import webbrowser
import clipboard
import urllib
import urlparse
import time

def path2url(path):
	w = os.path.join(os.path.expanduser("~/Documents"),path )
	return urlparse.urljoin('file:', urllib.pathname2url(w))
	
class MyView(ui.View):
	def will_close(self):
		pass
		
def oui_action(sender):
	global button_pressed,file_txt,file_html
	os.rename(file_txt,file_html)
	button_pressed = True
	
def non_action(sender):
	global button_pressed,file_txt
	os.remove(file_txt)
	button_pressed = True
	
def main():
	global button_pressed,file_txt,file_html
	
	console.clear()
	
	if appex.is_running_extension():
		url = appex.get_url()
	else:
		url = clipboard.get()
		
	if url == None:
		console.alert('Nothing in the ClipBoard','','Ok',hide_cancel_button=True)
		return
		
	if url[:7] <> 'http://' and url[:8] <> 'https://':
		console.alert('ClipBoard does not contain a valid URL','','Ok',hide_cancel_button=True)
		return
		
	# Webview to display conversion site
	x = 0
	y = 0
	w = back.width
	h = back.height - 32 - 2*10
	
	web = ui.WebView(name='web',frame=(x,y,w,h))
	web.border_color = 'blue'
	web.border_width = 1
	back.add_subview(web)
	
		# Label to display progress
	titlbl = ui.Label(name='titlbl')
	titlbl.width = back.width - 80*2 - 10*4
	titlbl.height = 32
	titlbl.x = 80 + 10*2
	titlbl.y = web.y + web.height + 10
	titlbl.text = ''
	titlbl.alignment = ui.ALIGN_CENTER
	titlbl.font= ('Courier-Bold',20)
	titlbl.text_color = 'black'
	back.add_subview(titlbl)
	
	# Button: yes
	oui_button = ui.Button()
	oui_button.border_color = 'black'
	oui_button.border_width = 1
	oui_button.width = 80
	oui_button.height = 32
	oui_button.x = web.x + web.width - 80 - 10
	oui_button.y = titlbl.y
	oui_button.title = 'yes'
	oui_button.alignment = ui.ALIGN_CENTER
	oui_button.font = ('Courier',20)
	oui_button.text_color = 'black'
	oui_button.hidden = False
	oui_button.action = oui_action
	back.add_subview(oui_button)
	
	# Button: non
	non_button = ui.Button()
	non_button.border_color = 'black'
	non_button.border_width = 1
	non_button.width = 80
	non_button.height = 32
	non_button.x = 10
	non_button.y = titlbl.y
	non_button.title = 'Non'
	non_button.alignment = ui.ALIGN_CENTER
	non_button.font = ('Courier',20)
	non_button.text_color = 'black'
	non_button.hidden = False
	non_button.action = non_action
	back.add_subview(non_button)
	
	
	# Read page contents
	r = requests.get(url)
	source = r.text
	ct = r.headers['Content-Type']
	extension = '.html' if ct.startswith('text/html') else '.txt'
	# Where to save the source
	filename='View-OpenPageSource'
	file_txt = os.path.abspath(filename+'.txt')
	file_html = os.path.abspath(filename+'.html')
	# Save the source
	with open(file_txt,'w') as f:
		f.write(source)
	# Display the source
	web.load_url(path2url(file_txt))
	
	# Ask if source file to be kept
	titlbl.text = 'Keep the souce file?'
	# loop button not pressed
	button_pressed = False
	while not button_pressed:
		time.sleep(0.5)
		
	back.close()
	
# Normally called by sharing action in Safari, but could be called by Launcher and passing url via clipboard

# Hide script
back = MyView()
back.background_color='white'
back.name = 'View/Open Page Source'

if appex.is_running_extension():
	disp_mode = 'sheet'
else:
	disp_mode = 'full_screen'
back.present(disp_mode,hide_title_bar=False)

# check if the script is running instead of     be imported
if __name__ == '__main__':
	main()
	
if appex.is_running_extension():
	appex.finish()
else:
	# Back to home screen
	webbrowser.open('launcher://crash')
# --------------------

