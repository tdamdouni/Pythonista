#coding: utf-8

import appex, os, console

def save():
	if appex.is_running_extension():
		sFp = appex.get_file_path()
		if sFp:
			console.hud_alert('Saving...')
			with open(sFp, 'rb') as f1:
				with open(os.path.basename(sFp), 'wb') as f2:
					f2.write(f1.read())
			console.hud_alert('Saved')
			
if __name__ == '__main__':
	save()

