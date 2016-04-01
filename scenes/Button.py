# code gebastelt (http://omz-forums.appspot.com/pythonista/post/5262856329101312)
# von @tdamdouni
# am 4/5/15 um 01:07

# coding: utf-8

import ui
import os

__SWATCH_PATH__ = os.path.expanduser('~/Documents/Dropbox/Images/')

def get_image(file_name):
	return ui.Image.named(__SWATCH_PATH__  + file_name)

class ButtonTest(object):
	
		def __init__(self):
			self.view = ui.load_view('ButtonTest')
			self.button = self.view['button1']
			self.button.background_image = get_image("image000.jpg")
			#self.button.background_image = ui.Image.named("image000.jpg")
			self.view.present('full_screen')

ButtonTest()