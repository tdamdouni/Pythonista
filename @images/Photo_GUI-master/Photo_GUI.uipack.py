# -*- coding: utf-8 -*-
###############################################################################
# This is a self-extracting UI application package for Photo_GUI.
# Run this script once to extract the packaged application.
# The files will be extracted to Photo_GUI.py and Photo_GUI.pyui.
# Make sure that these files do not exist yet.
# To update from an older version, move or delete the old files first.
# After extracting, the application can be found at Photo_GUI.py.
# This bundle can be deleted after extraction.
###############################################################################
# Packaged using PackUI by dgelessus
# https://github.com/dgelessus/pythonista-scripts/blob/master/UI/PackUI.py
###############################################################################
import console, os.path
NAME     = "Photo_GUI"
PYFILE   = """# coding: utf-8

import ui, io
import PIL
import photos
import Image, ImageOps, ImageFilter
import StringIO
import ImageEnhance
import console
from matplotlib import colors
from ColorMix import *
import clipboard
import sys


# Image converters
## Image must be one format to edit and another format to be displayed
def pil2ui(imgIn):#Thanks #@jmv38
	with io.BytesIO() as bIO:
		imgIn.save(bIO, 'PNG')
		imgOut = ui.Image.from_data(bIO.getvalue())
	del bIO
	return imgOut

def ui2pil(imgIn):#Thanks #@jmv38
	memoryFile = StringIO.StringIO(imgIn.to_png())
	imgOut = Image.open(memoryFile)
	imgOut.load()
	memoryFile.close()
	return imgOut

# /Image Converters


# Main window options

@ui.in_background
def get_img(sender):
	#v = sender.superview
	frame = root #imageview
	s = stack
	u = unstack
	try:
		photo = ui.Image.from_data(photos.pick_image(raw_data=True))
	except: return
	
	adjust_frame_size(photo)

	frame.image = photo
	s[:] = []
	u[:] = []

	s.append(frame.image)

def edit(sender):
	ev.present(hide_title_bar=True)

def undo(sender):
	frame = root
	s,u = stack,unstack
	if len(s) <= 1:
		console.hud_alert('Nothing to Undo','error')
	if len(s) > 1:
		u.append(s.pop())
		adjust_frame_size(s[-1])
		frame.image = s[-1]
	else:
		frame.image = s[0]

def redo(sender):
	frame = root
	s,u = stack,unstack
	if len(u) > 0:
		s.append(u.pop())
		adjust_frame_size(s[-1])
		frame.image = s[-1]
	else:
		console.hud_alert('Nothing to Redo','error')

def save(sender):
	v = sender.superview
	frame = root
	photo = ui2pil(frame.image)
	photos.save_image(photo)
	console.hud_alert('Saved','success')

def exit(sender):
	ev.close()
	pv.close()
	v.close()

# /Main window options



# Edit window options

#def cancel(ea):
#   ev.close()
##### built directly into edit_action()
##### may/not keep it there

def blur(ea):
	photo = ea.filter(ImageFilter.BLUR)
	edit_complete(photo)

def contour(ea):
	photo = ea.filter(ImageFilter.CONTOUR)
	edit_complete(photo)

def detail(ea):
	photo = ea.filter(ImageFilter.DETAIL)
	edit_complete(photo)

def edge_enhance(ea):
	photo = ea.filter(ImageFilter.EDGE_ENHANCE)
	edit_complete(photo)

def edge_enhance_more(ea):
	photo = ea.filter(ImageFilter.EDGE_ENHANCE_MORE)
	edit_complete(photo)

def emboss(ea):
	photo = ea.filter(ImageFilter.EMBOSS)
	edit_complete(photo)

def find_edges(ea):
	photo = ea.filter(ImageFilter.FIND_EDGES)
	edit_complete(photo)

def grayscale(ea):
	photo = ImageOps.grayscale(ea)
	edit_complete(photo)

def invert(ea):
	photo = ImageOps.invert(ea)
	edit_complete(photo)

def posterize(ea):
	photo = ImageOps.posterize(ea, 2)
	edit_complete(photo)

def rotate(ea):
	photo = ea.rotate(-90)
	edit_complete(photo)

def sharpen(ea):
	photo = ea.filter(ImageFilter.SHARPEN)
	edit_complete(photo)

def smooth(ea):
	photo = ea.filter(ImageFilter.SMOOTH)
	edit_complete(photo)

def smooth_more(ea):
	photo = ea.filter(ImageFilter.SMOOTH_MORE)
	edit_complete(photo)

def solarize(ea):
	photo = ImageOps.solarize(ea, 128)
	edit_complete(photo)


def colorbutton(ea): # for colorize()
	v = ea.superview
	c = colorbool
	if v.name == 'blackview':
		c[:] = []
		c.append(True)
		pvr.background_color = evroot1.background_color
		pv['slider1'].value = pv['view1'].background_color[0]
		pv['slider2'].value = pv['view1'].background_color[1]
		pv['slider3'].value = pv['view1'].background_color[2]
	if v.name == 'whiteview':
		c[:] = []
		c.append(False)
		pvr.background_color = evroot2.background_color
		pv['slider1'].value = pv['view1'].background_color[0]
		pv['slider2'].value = pv['view1'].background_color[1]
		pv['slider3'].value = pv['view1'].background_color[2]
	pv.present()

def select(colormixer):
	v = colormixer.superview
	c = colorbool
	color = v['view1'].background_color
	if c[0] == True:
		evroot1.background_color = color
	if c[0] == False:
		evroot2.background_color = color
	v.close()

def colorize(ea):
	#get RGB's: Ugly, needs reworked
	color1 = evroot1.background_color
	color2 = evroot2.background_color
	c1,c2 = [],[]
	for x in color1:
		c1.append(x)
	for x in color2:
		c2.append(x)
	final1 = r1,g1,b1 = int(255*c1[0]),int(255*c1[1]),int(255*c1[2])
	final2 = r2,g2,b2 = int(255*c2[0]),int(255*c2[1]),int(255*c2[2])
	#Now for the regular stuff
	gray = ImageOps.grayscale(ea)
	photo = ImageOps.colorize(gray, final1, final2)
	edit_complete(photo)

def brightness(ea,x):
	if x == 'p':
		photo = ImageEnhance.Brightness(ea).enhance(1.1)
	else:
		photo = ImageEnhance.Brightness(ea).enhance(.9)
	edit_complete(photo)

def color(ea,x):
	if x == 'p':
		photo = ImageEnhance.Color(ea).enhance(1.1)
	else:
		photo = ImageEnhance.Color(ea).enhance(.9)
	edit_complete(photo)

def contrast(ea,x):
	if x == 'p':
		photo = ImageEnhance.Contrast(ea).enhance(1.1)
	else:
		photo = ImageEnhance.Contrast(ea).enhance(.9)
	edit_complete(photo)

def sharpness(ea,x):
	if x == 'p':
		photo = ImageEnhance.Sharpness(ea).enhance(1.5)
	else:
		photo = ImageEnhance.Sharpness(ea).enhance(.5)
	edit_complete(photo)

@ui.in_background
def minfilter(ea):
	#Would like to choose keyboard type
	value = console.input_alert('Enter Value','valid values: 3, 5, 7, 9,...','3','Do it!')
	photo = ea.filter(ImageFilter.MinFilter(int(value)))
	edit_complete(photo)

@ui.in_background
def medfilter(ea):
	value = console.input_alert('Enter Value','valid values: 3, 5, 7, 9,...','3','Do it!')
	photo = ea.filter(ImageFilter.MedianFilter(int(value)))
	edit_complete(photo)
	
@ui.in_background
def maxfilter(ea):
	value = console.input_alert('Enter Value','valid values: 3, 5, 7, 9,...','3','Do it!')
	photo = ea.filter(ImageFilter.MaxFilter(int(value)))
	edit_complete(photo)

@ui.in_background
def modfilter(ea):
	value = console.input_alert('Enter Value','valid values: 2, 3, 4, 5,...','3','Do it!')
	photo = ea.filter(ImageFilter.ModeFilter(int(value)))
	edit_complete(photo)

def resize(ea):
	size = w,h = ea.size
	w/=1.5
	h/=1.5
	newsize = (int(w),int(h))
	photo = ea.resize(newsize, Image.BILINEAR)
	scroll = scrollview
	size = w,h = photo.size
	root.height = h
	root.width = w
	scroll.content_size = size
	edit_complete(photo)

# /Edit options




def edit_action(sender):
	if sender.name == 'cancel':
		ev.close()
		return

	x = root.image
	photo = ui2pil(x)
	if sender.title == '':
		x = sender.name[-1]
		globals()[sender.name[:-1]](photo,x)
	else:
		globals()[sender.name](photo)

def edit_complete(edited):
	pic = pil2ui(edited)
	frame = root
	s = stack
	s.append(pic)
	frame.image = s[-1]
	ev.close()


def adjust_frame_size(photo):
	size = w,h = photo.size
	scroll = scrollview
	root.height = h
	root.width = w
	scroll.content_size = size


#Standard globals
v = ui.load_view('Photo_GUI')
ev = ui.load_view('Photo_GUI_Edit')
pv = ui.load_view('ColorMix')
root = v['scrollview']['imageview']
scrollview = v['scrollview']
evroot1 = ev['editscroll']['blackview']
evroot2 = ev['editscroll']['whiteview']
pvr = pv['view1']
mainscroll = v['mainscroll']
mainscroll.shows_horizontal_scroll_indicator = False

#Would like to set True. Would first like to customize paging size/index.
mainscroll.paging_enabled = False

scrollview.shows_horizontal_scroll_indicator = False
scrollview.shows_vertical_scroll_indicator = False
#Extra globals
stack = []          #Undo()
unstack = []        #Redo()
colorbool = []  #Colorize()

def main():

	v.present(hide_title_bar=True)

if __name__ == '__main__':
	main()
"""
PYUIFILE = """[{"class":"View","attributes":{"name":"Photo GUI","background_color":"RGBA(1.000000,1.000000,1.000000,1.000000)","tint_color":"RGBA(0.000000,0.478000,1.000000,1.000000)","enabled":true,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","flex":""},"frame":"{{0, 0}, {320, 568}}","nodes":[{"class":"ScrollView","attributes":{"enabled":true,"flex":"WHLR","content_width":320,"name":"scrollview","content_height":510,"border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","uuid":"FE45B9B7-15A3-4CDB-AC09-F877DBE8E49C"},"frame":"{{0, 18}, {320, 516}}","nodes":[{"class":"ImageView","attributes":{"name":"imageview","uuid":"FD97562B-8ABA-4EFC-8FE9-A443F6F4FF39","enabled":true,"border_width":1,"border_color":"RGBA(0.000000,1.000000,0.920000,1.000000)","flex":""},"frame":"{{0, 0}, {320, 510}}","nodes":[]}]},{"class":"ScrollView","attributes":{"enabled":true,"flex":"WLRT","content_width":554,"name":"mainscroll","content_height":20,"border_color":"RGBA(0.000000,0.000000,0.000000,0.000000)","border_width":1,"uuid":"EE59A64F-0231-4F8A-8722-B501B62BEBF0"},"frame":"{{10, 542}, {300, 20}}","nodes":[{"class":"Button","attributes":{"background_color":"RGBA(0.642857,0.642857,0.642857,1.000000)","image_name":"ionicons-ios7-albums-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","tint_color":"RGBA(0.000000,0.940000,1.000000,1.000000)","action":"get_img","font_bold":true,"name":"get img","border_width":1,"uuid":"4E8AA111-6C8C-4B77-AAB4-D4D0F1240F9C","corner_radius":5},"frame":"{{6, 0}, {74, 20}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.642857,0.642857,0.642857,1.000000)","image_name":"ionicons-gear-a-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"R","tint_color":"RGBA(0.000000,0.000000,1.000000,1.000000)","action":"edit","font_bold":true,"name":"edit","border_width":1,"uuid":"A3D414E4-308B-4930-A668-54B0C282680C","corner_radius":5},"frame":"{{88, 0}, {80, 20}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.642857,0.642857,0.642857,1.000000)","image_name":"ionicons-ios7-undo-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"R","tint_color":"RGBA(0.000000,0.000000,1.000000,1.000000)","action":"undo","font_bold":true,"name":"undo","border_width":1,"uuid":"7E4CCF52-E3AF-4D69-B1D3-45D1C380E77F","corner_radius":5},"frame":"{{176, 0}, {80, 20}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.642857,0.642857,0.642857,1.000000)","image_name":"ionicons-ios7-redo-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"R","tint_color":"RGBA(0.000000,0.000000,1.000000,1.000000)","action":"redo","font_bold":true,"name":"redo","border_width":1,"uuid":"A157E008-E708-4229-9F19-8FFB2199ABAE","corner_radius":5},"frame":"{{264, 0}, {80, 20}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.642857,0.642857,0.642857,1.000000)","image_name":"ionicons-checkmark-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","tint_color":"RGBA(0.000000,1.000000,0.000000,1.000000)","action":"save","font_bold":true,"name":"save","border_width":1,"uuid":"48873CB7-F04C-4F8F-9940-DC6E2E4F791F","corner_radius":5},"frame":"{{352, 0}, {80, 20}}","nodes":[]},{"class":"Button","attributes":{"background_color":"RGBA(0.642857,0.642857,0.642857,1.000000)","image_name":"ionicons-close-round-32","border_color":"RGBA(0.000000,0.000000,0.000000,1.000000)","font_size":15,"title":"","enabled":true,"flex":"","tint_color":"RGBA(1.000000,0.000000,0.000000,1.000000)","action":"exit","font_bold":true,"name":"exit","border_width":1,"uuid":"B760F807-C8E9-4A0D-A823-418E1EC8132E","corner_radius":5},"frame":"{{440, 0}, {74, 20}}","nodes":[]}]}]}]"""
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
