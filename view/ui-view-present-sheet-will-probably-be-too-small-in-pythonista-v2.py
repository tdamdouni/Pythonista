# https://forum.omz-software.com/topic/2546/ui-view-present-sheet-will-probably-be-too-small-in-pythonista-v2

view.present('sheet')

# --------------------

view.width = view.height = min(ui.get_screen_size())
view.present('sheet')

# --------------------

def __init__(self):
	# ...
	self.present('sheet')
	
# --------------------

def did_load(self):
	# ...
	self.present('sheet')
	
# --------------------

