# https://forum.omz-software.com/topic/3808/shut-off-swipe-to-delete-with-list_dialogs

# bug

import dialogs

list = ['Apple', 'Orange', 'Pear']
selected = dialogs.list_dialog(title='Fruit', items=list, multiple=False)

# workaround

def list_dialog(title='', items=None, multiple=False, done_button_title='Done'):
	c = dialogs._ListDialogController(title, items, multiple, done_button_title=done_button_title)
	c.view.data_source.delete_enabled = False
	c.view.present('sheet')
	c.view.wait_modal()
	return c.selected_item


