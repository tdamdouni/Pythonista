# https://forum.omz-software.com/topic/4097/home-screen-alias-is-script-already-running/3

import builtins

if name == 'main':

	try:
		v=builtins.theview
	except:
		v=None
	
	if(isinstance(v,ui.View) and v.on_screen ):
	#console.hud_alert('reuse view')
		else:
			#console.hud_alert('create view')
			v = ui.load_view()
			v.present('sheet')
			builtins.theview=v

