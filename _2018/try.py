import ui
from ui import *

def button_action(sender):
	'@type sender: ui.Button'
	# get button title
	t = sender.title
	print(t)

v = ui.load_view('try')
v.present('sheet')
