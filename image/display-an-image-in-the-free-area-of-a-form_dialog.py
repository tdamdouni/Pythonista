# coding: utf-8

# https://forum.omz-software.com/topic/3064/display-an-image-in-the-free-area-of-a-form_dialog

def myform_dialog(title='', fields=None,sections=None, done_button_title='Done',cover=None):

	sections = [('', fields)]
	c = dialogs._FormDialogController(title, sections, done_button_title=done_button_title)
	y = 35
	for s in c.cells:
		for cell in s:
			y = y + cell.height
	if cover != None:
		w = c.container_view.width
		h = c.container_view.height - y
		x = 0
		cover_image = ui.ImageView(frame=(x,y,w,h))
		cover_image.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
		cover_image.image = ui.Image.from_data(cover)
		c.container_view.add_subview(cover_image)
		
	c.container_view.present('sheet')
	c.container_view.wait_modal()
	# Get rid of the view to avoid a retain cycle:
	c.container_view = None
	if c.was_canceled:
		return None
	return c.values

