# -*- coding: utf-8 -*-

# https://github.com/mncfre/Save_Videos

###############################################################################
# This is a self-extracting UI application package for YoutubeNow2.
# Run this script once to extract the packaged application.
# The files will be extracted to YoutubeNow2.py and YoutubeNow2.pyui.
# Make sure that these files do not exist yet.
# To update from an older version, move or delete the old files first.
# After extracting, the application can be found at YoutubeNow2.py.
# This bundle can be deleted after extraction.
###############################################################################
# Packaged using PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
###############################################################################

import console, os.path

NAME     = "YoutubeNow2"
PYFILE   = """#coding: utf-8
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
"""
PYUIFILE = """[{"class":"View","attributes":{"tint_color":"RGBA(0.000000,0.478000,1.000000,1.000000)","enabled":true,"flex":"","name":"Video Downloader","corner_radius":0,"border_width":0,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alpha":1,"background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)"},"frame":"{{0, 0}, {320, 295}}","nodes":[{"class":"Switch","attributes":{"tint_color":"RGBA(0.428571,0.622857,1.000000,1.000000)","enabled":true,"flex":"","name":"audio","value":false,"alpha":1,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","uuid":"35D3D800-3EA1-4A35-8C45-7DFD02CF829F"},"frame":"{{117.5, 95}, {51, 31}}","nodes":[]},{"class":"Label","attributes":{"font_size":17,"enabled":true,"text":"Audio Only:","flex":"","name":"label1","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"12C76330-FDB6-4655-8ED4-5B8510A7EEC1"},"frame":"{{12, 95}, {97.5, 31}}","nodes":[]},{"class":"TextField","attributes":{"alignment":"left","autocorrection_type":"no","font_size":14,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","enabled":true,"tint_color":"RGBA(0.142857,0.391428,1.000000,1.000000)","flex":"W","text_color":"RGBA(0.285714,0.521428,1.000000,1.000000)","alpha":1,"name":"urlfield","border_style":3,"spellchecking_type":"no","uuid":"9E4D7752-B705-449E-82AE-616BC9360FD4","border_width":1,"corner_radius":5},"frame":"{{6, 42}, {266, 32}}","nodes":[]},{"class":"Label","attributes":{"font_size":20,"enabled":true,"text":"Video URL:","flex":"","name":"label2","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"4E32B09F-95C3-4B5B-A941-28F41A5BF521"},"frame":"{{105, 6}, {102.5, 32}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.857143,0.857143,0.857143,1.000000)","image_name":"ionicons-archive-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"Download","enabled":true,"flex":"","action":"download","font_bold":false,"name":"download","corner_radius":5,"border_width":1,"uuid":"68C2B56A-C000-42AC-B9E0-8AC93857F792"},"frame":"{{6, 249}, {308, 40}}","nodes":[]},{"class":"Slider","attributes":{"enabled":true,"flex":"W","name":"quality","continuous":true,"value":1,"action":"slider_action","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","uuid":"11E23EBA-50E6-4632-8BC1-B18535A38E1B"},"frame":"{{12, 174}, {298, 34}}","nodes":[]},{"class":"Label","attributes":{"font_size":17,"enabled":true,"text":"Quality:","flex":"","name":"label3","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"E7251ED4-423D-489C-88F1-D555065A4CD6"},"frame":"{{12, 134}, {61, 32}}","nodes":[]},{"class":"Label","attributes":{"font_size":17,"enabled":true,"text":"Best","font_name":"<System-Bold>","name":"qualityopt","flex":"","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","alpha":1,"uuid":"0564B50D-8F82-4D55-8805-0EEAD7F9DB65"},"frame":"{{81, 134}, {150, 32}}","nodes":[]},{"class":"Label","attributes":{"font_size":17,"enabled":true,"text":"Low","flex":"","name":"label4","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"799CA2DE-9C26-4FAF-A19B-7C710ED8BA8C"},"frame":"{{12, 209}, {39, 32}}","nodes":[]},{"class":"Label","attributes":{"font_size":17,"enabled":true,"text":"Medium","flex":"","name":"label5","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"CF8D67D4-8672-4FB5-AB22-27275493CA71"},"frame":"{{122, 204}, {70.5, 37}}","nodes":[]},{"class":"Label","attributes":{"font_size":17,"enabled":true,"text":"Best","flex":"","name":"label6","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","text_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","alignment":"left","uuid":"764FD3F3-9060-4F16-A0B2-15F29A4AFF4B"},"frame":"{{257, 209}, {46, 32}}","nodes":[]},{"class":"Button","attributes":{"image_name":"ionicons-clipboard-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","action":"paste_tapped","font_bold":false,"name":"paste","border_width":0,"uuid":"0F5C8FB1-9969-45E0-BDB1-41902D316A3E","corner_radius":5},"frame":"{{280, 42}, {29, 32}}","nodes":[]}]}]"""

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