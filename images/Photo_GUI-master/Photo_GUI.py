# coding: utf-8

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
