# https://pythonista-app.slack.com/archives/codinghelp/p1486406610001343?thread_ts=1486404305.001339&cid=C14HM3ZC6

# @dgelessus

import ui

message = 'Beep'

def scrollview(message):
	sv = ui.ScrollView()
	sv.frame = (10, 10, 380, 380)
	sv.content_size = 380, 800
	view.add_subview(sv)
	
	tv = ui.TextView()
	tv.frame = (10, 10, 380, 380)
	tv.font = ('Palatino', 18)
	tv.editable = False
	tv.text = message
	sv.add_subview(tv)
	
view = ui.View()
view.name = 'Demo'
view.background_color = 'blue'
view.frame=(0, 0, 400, 400)

scrollview(message)

view.present(orientations = 'portrait')

