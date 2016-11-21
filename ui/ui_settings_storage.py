# coding: utf-8

# https://github.com/jsbain/uicomponents/blob/master/ui_settings_storage.py

# https://forum.omz-software.com/topic/3027/saving-pythonista-app-switch-and-button-states/9

# Here is a more flexible method, intended to be used with @brumm's approach. Create a custom attribute "stored" (either programmatically or in ui editor), then this method creates a dict heirarchy of all storable elements. Supports deep heirarchies, and multiple components. Ideally each component and container view has a name attribute. it will create a temporary key if it does not (but if you change the ui later, such that subviews are added in different order, it will most likely fail to restore).

# Incidentally... json does not let you use non-string dict keys... the above approch uses yaml, which is similar, but faithfully reproduces the dicts.

import ui
def store_settings(view):
	'''return a dictionary suitable for storing as json or other method, which stores the value,selected_index,or text attribute of any ui component that has a stored attribute set True'''
	if getattr(view,'subviews',False):
		output={}
		for i,sv in enumerate(view.subviews):
			output_tmp=store_settings(sv)
			if output_tmp:
				if sv.name:
					key=sv.name
				else:
					key=i #need json keys to be str
				output[key]=output_tmp
		return output
	else:
		if getattr(view,'stored',False):
			if hasattr(view,'value'):
				return view.value
			elif hasattr(view,'selected_index'):
				return view.selected_index
			elif hasattr(view,'text'):
				return view.text
				
def restore_settings(view, stored_value):
	'''restore settings to viee from the stored settings.  stored_value should be a dict returned from store_settings.'''
	for i,sv in enumerate(view.subviews):
		if sv.name:
			key=sv.name
		else:
			key=i
		try:
			restore_settings(sv,stored_value[key])
		except KeyError:
			pass
	if hasattr(view,'value'):
		view.value=stored_value
	elif hasattr(view,'selected_index'):
		view.selected_index=stored_value
	elif hasattr(view,'text'):
		view.text=stored_value
		
		
if __name__=='__main__':
	'''example usage'''
	def createView():
		main=ui.View(frame=(0,0,576,576))
		subpanel=ui.View(frame=(0,330,576,246))
		subpanel2=ui.View(frame=(0,0,576,246))
		slider=ui.Slider(frame=(10,10,150,44),name='slider1')
		slider.stored=True
		switch1=ui.Switch(frame=(10,66,70,44),name='switch1')
		switch1.stored=True
		switch2=ui.Switch(frame=(90,66,70,44)) #no name
		switch2.stored=True
		switch3=ui.Switch(frame=(10,120,70,44),name='switch3') #not stored
		tf1=ui.TextField(frame=(10,180,250,50),name='textfield')
		tf1.stored=True
		main.add_subview(subpanel)
		subpanel.add_subview(slider)
		subpanel.add_subview(switch1)
		subpanel.add_subview(switch2)
		subpanel.add_subview(switch3)
		subpanel.add_subview(tf1)
		slider2=ui.Slider(frame=(10,10,150,44),name='slider1')
		slider2.stored=True
		subpanel2.add_subview(slider2)
		main.add_subview(subpanel2)
		return main
	v=createView()
	v.present('sheet')
	v.wait_modal()
	saved=store_settings(v)
	import yaml
	saved_yaml=yaml.dump(saved)
	#...
	v2=createView()
	restore_settings(v2,yaml.load(saved_yaml))
	v2.present('sheet')

