# https://forum.omz-software.com/topic/4172/customizing-of-dialogs-form/2

import ui
import dialogs
def myform_dialog(title='', fields=None,sections=None, done_button_title='ok'):
	global c
	
	sections = [('', fields)]
	c = dialogs._FormDialogController(title, sections, done_button_title=done_button_title)
	
	c.container_view.frame = (0, 0, 500,900)
	c.container_view.present('sheet')
	c.container_view.wait_modal()
	# Get rid of the view to avoid a retain cycle:
	c.container_view = None
	if c.was_canceled:
		return None
	return c.values
	
fields = [{'title':'title','type':'text','value':''}]
f = myform_dialog(title='dialog title', done_button_title='ok',fields=fields, sections=None)

