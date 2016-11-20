# https://gist.github.com/balachandrana/6c8617382079e4486b12a4dd35f5c8c5

# https://forum.omz-software.com/topic/3653/how-to-tell-a-textview-to-scroll

import ui
import sys


class TextViewFile(object):
	def __init__(self, textview):
		self.textview = textview
		
	def write(self, msg):
		self.textview.text += msg
		scroll()
		
backup_stdout = None


def button_action(sender):
	print(sender.title + ' pressed')
	
def segmentedcontrol_action(sender):
	global backup_stdout
	
	if sender.selected_index == 1:
		if not backup_stdout:
			backup_stdout = sys.stdout
			sys.stdout = textview_stdout
	else:
		if backup_stdout:
			sys.stdout = backup_stdout
			backup_stdout = None
			
class CloseView(ui.View):
	def __init__(self):
		super().__init__()
		
	def will_close(self):
		global backup_stdout
		
		sys.stdout = backup_stdout
		backup_stdout = None
		
v = ui.load_view()
v['textview1'].text = '''
****************
Button press events
are logged in console
or TextView based on
respective tab
selection
*****************
'''
textview_stdout = TextViewFile(v['textview1'])
v['segmentedcontrol1'].selected_index = 0
v['segmentedcontrol1'].action = segmentedcontrol_action

@ui.in_background
def scroll():
	v['textview1'].content_offset = (0, v['textview1'].content_size[1] -v['textview1'].height)
	
clv = CloseView()
clv.width, clv.height = v.width, v.height
clv.add_subview(v)

clv.present('sheet')

