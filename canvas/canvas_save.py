# coding: utf-

# https://gist.github.com/jsbain/389a67c5aacb097b87fd

from __future__ import print_function
from objc_util import *
import canvas
import os
def save_canvas_to_png(filename):
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	image=rootVC.accessoryViewController().consoleViewController().canvasImageView().image()
	if image:
		data=ObjCInstance(c.UIImagePNGRepresentation(image))
		data.writeToFile_atomically_(os.path.abspath(filename),True)
	else:
		print('canvas was empty')
if __name__=='__main__':
	#Draw a red circle filling the entire canvas
	import canvas
	w = h = 512
	canvas.set_size(w, h)
	canvas.set_fill_color(1, 0, 0)
	canvas.fill_ellipse(0, 0, w, h)
	save_canvas_to_png('canvas.png')

