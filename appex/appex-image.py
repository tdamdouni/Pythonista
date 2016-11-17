# coding: utf-8

# https://forum.omz-software.com/topic/3520/gives-an-error-at-the-line-that-i-marked

import ui
import appex
import Image


v = ui.load_view()
#img = appex.get_image()
#if img:
	#v["image"].image = ui.Image(str(img)) #Error occurs here, it says IOError couldn't display image or something like that
img_data = appex.get_image_data()
if img_data:
	v['image'].image = ui.Image.from_data(img_data)
# ...
v.present('sheet')
if not img:
	v.close()

