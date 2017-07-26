# coding: utf-8

# https://gist.github.com/philgruneich/32c1568fd1feb61487a3

import reminders
import sys
import dialogs
import webbrowser
from urllib import quote

def completeReminder():

	_title = sys.argv[1] if len(sys.argv) > 1 else None
	_list = sys.argv[2] if len(sys.argv) > 2 else None

	if _list:
		calendars = reminders.get_all_calendars()
		_list = [x for x in calendars if x.title == _list]
		_list_title = _list[0].title
		todo = reminders.get_reminders(completed=False, calendar=_list[0])
		callback = 'twodo://x-callback-url/showList?name=%s' % quote(_list_title)
	else:
		todo = reminders.get_reminders(completed=False)
		callback = 'twodo://'
	
	if len(todo) == 0:
		return dialogs.hud_alert('You don\'t have any reminder left to do.')
	
	if _title:
		
		this = [x for x in todo if x.title == _title]
		
		if len(this) == 1:
			this = this[0]
		elif len(this) <= 0:
			return dialogs.hud_alert('You don\'t have any reminder matching these terms.')
		else:
			todomap = {x.title: x for x in this}
			this = dialogs.list_dialog('Multiple matches', todomap.keys())
			
			if not this:
				return dialogs.hud_alert('You gotta pick the correct reminder.')
			else:
				this = todomap.get(this)
				
	else:
		todomap = {x.title: x for x in todo}
		this = dialogs.list_dialog('Multiple matches', todomap.keys())
			
		if not this:
			return dialogs.hud_alert('You gotta pick the correct reminder.')
		else:
			this = todomap.get(this)
	
	this.completed = True
	this.save()
	webbrowser.open(callback)
		

if __name__ == '__main__':
	completeReminder()
		
