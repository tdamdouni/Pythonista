# coding: utf-8

# https://forum.omz-software.com/topic/3045/unable-to-get-scrollview-working/14

import ui
import ping
import base64
from PIL import Image
import StringIO
import re

w = ui.View()
sv = ui.ScrollView()
v = ui.View()
#v.present('fullscreen')
t = None
def BuildServerList(Servers):
	global t
	lasty = 10
	for Server in Servers:
		server = ui.load_view('MCServer.pyui')
		server['title'].text=Server['title']
		server.name = Server['title']
		server.background_color = (.1,.1,.1,1)
		try:
			temp = ping.do_ping(Server['ip'],Server['port'])
			server['ping'].text = str(temp[0])+' ms'
			server['Description'].text =re.sub(u'\u00A7.', '',temp[1].response['description'])
			server['Version'].text =str(temp[1].response['version']['name'])
			server['player'].text = str(temp[1].response['players']['online'])+' / '+str(temp[1].response['players']['max'])
			if temp[0] < 150:
				server['bars'].image = ui.Image.named('0.PNG')
			elif temp[0]<300:
				server['bars'].image = ui.Image.named('1.PNG')
			elif temp[0]<600:
				server['bars'].image = ui.Image.named('2.PNG')
			elif temp[0]<1000:
				server['bars'].image = ui.Image.named('3.PNG')
			else:
				server['bars'].image = ui.Image.named('4.PNG')
		except Exception as e:
			try:
				temp = ping.do_ping(Server['ip'],Server['port'])
				server['ping'].text = str(temp[0])+' ms'
				server['Description'].text =re.sub(u'\u00A7.', '',str(temp[1].response['description']['text']))
				server['Version'].text =str(temp[1].response['version']['name'])
				server['player'].text = str(temp[1].response['players']['online'])+' / '+str(temp[1].response['players']['max'])
				if temp[0] < 150:
					server['bars'].image = ui.Image.named('0.PNG')
				elif temp[0]<300:
					server['bars'].image = ui.Image.named('1.PNG')
				elif temp[0]<600:
					server['bars'].image = ui.Image.named('2.PNG')
				elif temp[0]<1000:
					server['bars'].image = ui.Image.named('3.PNG')
				else:
					server['bars'].image = ui.Image.named('4.PNG')
			except:
				server['Description'].text = 'Ping Timeout'
				server['bars'].image = ui.Image.named('5.PNG')
		try:
			test = ui.Image.from_data(base64.decodestring(temp[1].response['favicon'].split(',')[1]))
			server['image'].image = test
		except:
			server['image'].image  = ui.Image.named('unknown.png')
		server['bars'].image = ui.Image.named('0.PNG')
		server.x = 10
		server.y = lasty+10
		lasty = lasty+10 +server.height
		v.add_subview(server)
	v.background_color=(0,0,0,0)
	v.height = lasty
	v.width=730
	sv.add_subview(v)
	sv.x,sv.y = 0,0
	sv.content_size.height = lasty+10
	sv.content_size.width = 730
serverList = [{'title':'ORE School','ip':'nickstar.openredstone.org','port':25565},{'title':'ORE SkyBlock','ip':'nickstar.openredstone.org','port':26969},{'title':'PandoraCraft','ip':'173.236.23.173','port':25565},{'title':'ORE School','ip':'nickstar.openredstone.org','port':25565},{'title':'ORE SkyBlock','ip':'nickstar.openredstone.org','port':26969},{'title':'PandoraCraft','ip':'173.236.23.173','port':25565}]
BuildServerList(serverList)
sv.width,sv.height = ui.get_screen_size()
sv.border_color=(0,1,0,0)
sv.border_width = 10
w.background_color=(1,1,1,0)
w.add_subview(sv)
w.present()

# --------------------

import ui

if __name__ == '__main__':
	f = (0, 0, 600, 800)
	v = ui.View(frame = f, bg_color = 'teal')
	sv = ui.ScrollView(frame = f, bg_color = 'white')
	sv.content_size = (v.bounds.width, v.bounds.height * 4)
	v.add_subview(sv)
	
	v.present('sheet')
# --------------------

