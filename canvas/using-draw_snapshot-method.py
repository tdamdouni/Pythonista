# https://forum.omz-software.com/topic/3401/share-using-draw_snapshot-method

# Phuket2 , Pythonista Forums (Python profiency, not much)
# works for python 2 or 3

import ui, editor

def _make_button(title):
	btn = ui.Button()
	btn.width = 80
	btn.height = 32
	btn.border_width = .5
	btn.title = title
	return btn
	
def snapshot(obj):
	# return a ui.Image of the ui element passed (obj)
	with ui.ImageContext(obj.width, obj.height) as ctx:
		obj.draw_snapshot()
		return ctx.get_image()
		
def ui_image_to_file(img, fn):
	# write ui.Image, img to file fn
	if not type(img) is ui.Image:
		print('expected {}, but recieved {}. File not written'.format(ui.Image, type(img)))
		return False
		
	bytes = img.to_png()
	with open(fn , 'wb') as file:
		file.write(bytes)
		
	return True
	
	
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	v = ui.View(frame = f, bg_color = 'lightyellow')
	y = 10
	# add a row of stupid buttons to the view for an example
	for i in range(5):
		btn = _make_button('btn ' + str(i))
		btn.y = (y + (btn.height * i))
		v.add_subview(btn)
		# draw a view to the console
		snapshot(btn).show()
	v.present('sheet')
	
	
	#returns a ui.Image, .show() is to show it in the console
	img = snapshot(v)
	img.show()
	
	# write a ui.Image to a .png file
	ui_image_to_file(img, 'somestupidpng.png')
# --------------------

