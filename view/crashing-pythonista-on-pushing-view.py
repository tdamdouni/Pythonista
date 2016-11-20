# https://forum.omz-software.com/topic/3314/crashing-pythonista-on-pushing-view

import ui
import time
class source (object):
	def __init__(self):
		self.selectcb = None
	def tableview_number_of_rows(self, tv, s):
		return 1
	def tableview_cell_for_row(self, tv, s, r):
		cell = ui.TableViewCell()
		cell.text_label.text = 'DoubleTap'
		return cell
	def tableview_did_select(self, tv, s, r):
		self.selectcb()
		time.sleep(1)
		
view = ui.TableView()

s = source()

nav = ui.NavigationView(view)
w,h = ui.get_screen_size()
v2 = ui.View(frame=(0,0,w,h))
@ui.in_background
def cb():
	time.sleep(1)
	nav.push_view(v2)
	time.sleep(1)
s.selectcb = cb
view.data_source = s
view.delegate = s
nav.present()
# --------------------

