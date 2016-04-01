# coding: utf-8

# @omz twitter

# http://omz-software.com/share/PythonistaRainbowEditor.jpg

from objc_util import *
import ui
from random import random
from colorsys import hsv_to_rgb

@on_main_thread
def main():
	app = ObjCClass('UIApplication').sharedApplication()
	root_vc = app.keyWindow().rootViewController()
	main_view = root_vc.detailViewController().view()
	size = main_view.bounds().size
	for i in xrange(10):
	    w = size.width / 10
	    x = w * i
	    r, g, b = hsv_to_rgb(i/10.0, 1, 1)
	    iv = ui.ImageView(frame=(x, 0, w, 64), flex='WLR')
	    iv.background_color = (r, g, b)
	    iv.alpha = 0.25
	    main_view.addSubview_(iv)

main()