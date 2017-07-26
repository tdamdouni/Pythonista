# https://forum.omz-software.com/topic/4110/reading-pythonistas-apples-plist-file-format/2

import editor
import ui
import time

class SomeUi(ui.View):
	def __init__(self):
		self.frame = (0, 0, 500, 470)
		self.table_view = ui.TableView(frame=(10, 10, 480, 400))
		self.text_view = ui.TextField(frame=(10, 420, 480, 40))
		self.add_subview(self.table_view)
		self.add_subview(self.text_view)
		editor.apply_ui_theme(self)
		
def wait(dt=1.0):
	t = time.perf_counter()
	while time.perf_counter() - t < dt:
		pass
		
op = SomeUi()
op.present('sheet')
wait(3)
op.close()
wait(1)
editor.present_themed(op, style='sheet')

