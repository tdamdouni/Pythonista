# https://forum.omz-software.com/topic/3801/how-i-make-ui-buttons-and-link-them/5

import ui
label = ui.Label(text='Label', text_color = 'red')

def field_action(sender):
	label.text = sender.text
	
field = ui.TextField(text='Field', action=field_action, enabled=False)
field.y = label.y + label.height + 10

def button_action(sender):
	field.enabled = not field.enabled
	
button = ui.Button(title='Button', action=button_action)
button.y = field.y + field.height + 10

view = ui.View()
for subview in (label, field, button):
	view.add_subview(subview)
view.present()
# --------------------
import ui

class MyView(ui.View):
	def __init__(self):
		label = ui.Label(name='label', text='Label', text_color = 'red')
		field = ui.TextField(name='field', text='Field', delegate=self, enabled=False)
		field.y = label.y + label.height + 10
		button = ui.Button(title='Disabled', action=self.action)
		button.y = field.y + field.height + 10
		for subview in (label, field, button):
			self.add_subview(subview)
		self.present()
		
	def action(self, sender):
		self['field'].enabled = not self['field'].enabled
		sender.title = 'Enabled' if self['field'].enabled else 'Disabled'
		
	def textfield_did_change(self, textfield):
		self['label'].text = textfield.text
		
MyView()
# --------------------
import ui

locked = ui.Image.named('iow:locked_32')
unlocked = ui.Image.named('iow:unlocked_32')
view = ui.View()
field = ui.TextField(text='Field', enabled=False)
view.add_subview(field)

def action(sender):
	field.enabled = not field.enabled
	sender.image = unlocked if field.enabled else locked
	
view.add_subview(ui.Button(action=action, image=locked, name='button'))
view['button'].x = field.x + field.width + 10
view.present()
# --------------------

