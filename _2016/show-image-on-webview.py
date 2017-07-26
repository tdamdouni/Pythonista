# https://forum.omz-software.com/topic/3794/open-gif-or-image-in-safari/20

import ui
import os
class MyView(ui.View):
	def __init__(self,w,h):
		self.width = w
		self.height = h
		
		wv = ui.WebView(frame=(0,0,w,h))
		doc_path = os.path.expanduser('~/Documents')
		file_path = os.path.join(doc_path,'IMG_5126.JPG') # your file name of course
		wv.load_url('file://'+file_path)
		self.add_subview(wv)
		
#w, h = ui.get_screen_size()
w, h = (540,620)
back = MyView(w, h)
back.present('sheet')

