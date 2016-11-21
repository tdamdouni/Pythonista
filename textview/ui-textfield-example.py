import ui

w, h = ui.get_screen_size()

def textfield_action(sender):
	sender.superview['textview'].text += sender.text.strip() + '\n'
	sender.text = ''
	
view = ui.View(name='Type text in the textfield and hit return...')
view.add_subview(ui.TextView(frame=(0, 50, w, h-50), name='textview'))
view['textview'].editable = False
view.add_subview(ui.TextField(frame=(0, 0, w, 50), name='textfield'))
view['textfield'].action = textfield_action
view.present()

