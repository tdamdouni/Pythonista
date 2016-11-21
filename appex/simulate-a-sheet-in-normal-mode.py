# coding: utf-8

# https://forum.omz-software.com/topic/3282/simulate-a-sheet-in-normal-mode-your-opinion-please

import ui
import appex

class MyView(ui.View):
	def __init__(self,w,h):
		self.width = w
		self.height = h
	def will_close(self):
		global back,sheet
		if self == sheet:
			if appex.is_running_extension():
				# back ui.view does not exist
				appex.finish()
			else:
				back.close() # close back ui.view
				
def main():
	global back,sheet
	# Main code
	if not appex.is_running_extension():
		# Hide script
		w, h = ui.get_screen_size()
		back = MyView(w,h)
		back.present('full_screen'  , hide_title_bar=True)
		iv = ui.ImageView(frame=back.bounds)
		iv.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
		iv.image = ui.Image.named('Home Screen.png')
		back.add_subview(iv)
		
	# Create sheet ui.view
	w, h = (500,500)
	sheet = MyView(w,h)
	sheet.background_color='white'
	sheet.name = 'test'
	sheet.bring_to_front()
	sheet.present('sheet', hide_title_bar=False)
	
# Protect against import
if __name__ == '__main__':
	main()
# --------------------

