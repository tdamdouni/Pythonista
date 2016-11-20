# coding: utf-8

# https://gist.github.com/ejetzer/d276f1229d2cbb3b0f09

import appex, dialogs, scene
import plistlib, copy, webbrowser, urllib, time

# check out http://handleopenurl.com/

db = 'Tasks.txt'
url = 'omnifocus://task/%s'
due = 'due://x-callback-url/add?title=%s&hourslater=4&x-success=pythonista://&x-error=pythonista://&x-source=Pythonista'

TESTER = scene.Scene()
def p(): TESTER.paused = True
def r(): TESTER.paused = False
TESTER.pause = p
TESTER.resume = r

def get_tasks(shared):
	# [{'attachments': [{'com.omnigroup.omnifocus.ofaction': None, 'public.file-url': None}]}]
	tasks = shared[0]['attachments']
	tasks = (t['public.file-url'] for t in tasks)
	tasks = (open(n).read() for n in tasks)
	tasks = (plistlib.readPlistFromString(t) for t in tasks)
	# {'newActions': [{'name': 'None', 'uuid': 'None'}]}
	tasks = (t['newActions'][0] for t in tasks)
	tasks = ((t['name'], url % t['uuid']) for t in tasks)
	tasks = (' '.join(t) + '\n' for t in tasks)
	return tasks
	
def main():
	if not appex.is_running_extension():
		with open(db) as tasks:
			for task in tasks:
				task = urllib.quote(task)
				webbrowser.open(due % task)
				time.sleep(10)
				while TESTER.paused:
					time.sleep(2)
		open(db, 'w').close() # Erase file
	else:
		shared = appex.get_input()
		if shared: tasks = get_tasks(shared)
		with open(db, 'a') as dbfile:
			dbfile.writelines(tasks)
		#for task in tasks:
			#dialogs.share_text(task)
	dialogs.alert('Done!', '', 'Ok', hide_cancel_button=True)
	
if __name__ == '__main__':
	main()

