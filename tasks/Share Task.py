# coding: utf-8

# https://gist.github.com/ejetzer/875c4561194ff9c56beb

import appex, dialogs, scene
import plistlib, copy, webbrowser, urllib, time

# check out http://handleopenurl.com/

url = 'omnifocus://task/%s'

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
	if appex.is_running_extension():
		shared = appex.get_input()
		if shared: tasks = get_tasks(shared)
		for task in tasks:
			dialogs.share_text(task)
			
if __name__ == '__main__':
	main()

