# coding: utf-8

# https://forum.omz-software.com/topic/2543/pythonista-crashes-after-returning-from-share-extension-app

import ui
import dialogs

def button_action(sender):
	dialogs.share_text('test')
	
v = ui.View(frame=(0,0,200,400))
btn = ui.Button(title='button')
btn.action = button_action
btn.center = v.center
v.add_subview(btn)

if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present(style='full_screen', hide_title_bar=False, orientations=['portrait'])

