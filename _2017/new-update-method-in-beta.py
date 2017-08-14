# https://forum.omz-software.com/topic/4199/new-update-method-in-beta-just-curious

#import ui
#def myupdate():
	#print('in Update')
	
#v = ui.load_view()
#v.update_interval = 1
#v.update = myupdate
#v.present('sheet')

#print(v.update)


import ui
import types

class CustomView(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def update(self):
		pass
		
def myupdate(self):
	print('in Update')
	
def button_action(sender):
	s = sender.superview
	s['view1'].update_interval = 1
	s['view1'].update = types.MethodType(myupdate, s['view1'])
	#print(s['view1'].update)
	
v = ui.View(frame=(0,0,600,600))
v.add_subview(ui.Button(title='update', action=button_action))
v1 = CustomView(frame=(0,300,300,300), name='view1')
v.add_subview(v1)
v.present('sheet')

