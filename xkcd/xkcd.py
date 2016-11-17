# https://github.com/Ivoah/XKCD-viewer

import ui
import requests
import io
import dialogs
import random

def load_comic(view, num):
	req = requests.get('http://xkcd.com/{}/info.0.json'.format(num))
	if req.status_code == 200:
		view.current = num
		view['comic_num'].text = str(num)
		view['slider'].value = num/latest
		comic = req.json()
		
		view['title'].text = comic['title']
		#view['comic'].load_from_url(comic['img'])
		view['comic'].image = ui.Image.from_data(requests.get(comic['img']).content)
		
#@ui.in_background
def prev(sender):
	load_comic(sender.superview, sender.superview.current - 1)
	
#@ui.in_background
def next(sender):
	load_comic(sender.superview, sender.superview.current + 1)
	
#@ui.in_background
def slider_changed(sender):
	load_comic(sender.superview, int(latest*sender.value) if int(latest*sender.value) > 0 else 1)
	
def alt(sender):
	comic = requests.get('http://xkcd.com/{}/info.0.json'.format(sender.superview.current)).json()
	dialogs.alert(comic['title'], comic['alt'])
	
#@ui.in_background
def rand(sender):
	load_comic(sender.superview, random.randint(1, latest))
	
latest = requests.get('http://xkcd.com//info.0.json'.format(id)).json()['num']

v = ui.load_view()
v.current = latest
load_comic(v, v.current)
v.width = v.height = min(ui.get_screen_size())
v.present('sheet')

