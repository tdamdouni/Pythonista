# coding: utf-8

# https://github.com/MCS-Kaijin/iGitHub

# A python script written for Pythonista so that you can access and manage your GitHub account from your mobile device

import ui
import urllib
import zipfile

mb_isopen = False

def show_menu_bar(sender):
	global mb_isopen
	mb = sender.superview.superview["view2"]
	sb = mb["sb"]
	def animation():
		w = 20 if mb_isopen else 175
		mb.frame = (0, 65.5, w, 568)
		sb.frame = (0, 0, w, 568)
	ui.animate(animation, duration=1.0)
	if mb_isopen:
		mb.background_color = (0, 0, 0, 0)
		mb.border_color = (0, 0, 0, 0)
		mb.border_width = 0
		sb.alpha = 0
	else:
		mb.background_color = (1, 1, 1, 1)
		mb.border_color = (0, 0, 0, 1)
		mb.border_width = 1
		sb.alpha = 1
	mb_isopen = not mb_isopen
	
	
# 'Get Repository' options screen
gr_open = False
lbl1 = ui.Label()
lbl1.name = 'label1'
lbl1.text = 'User: '
lbl1.frame = (6,6,60,20)

usrt = ui.TextField()
usrt.frame = (66, 6, 150, 20)
usrt.name = 'usr'
usrt.autocapitalization_type = False
usrt.autocorrection_type = False

lbl2 = ui.Label()
lbl2.frame = (6,26,60,20)
lbl2.text = 'Repo: '
lbl2.name = 'label2'

psdt = ui.TextField()
psdt.name = 'rep'
psdt.frame = (66,26,150,20)
psdt.autocapitalization_type = False
psdt.autocorrection_type = False

btn = ui.Button()
btn.name = 'getrepo'
btn.title = 'Get Repo'
btn.frame = (6,52,75,20)
btn.background_color = 'green'
btn.tint_color = 'white'

# 'GitHub' screen. I can't currently afford a paid account so I can't integrate GitHub for real, but here's the website
gh_open = False
wv = ui.WebView()
wv.frame = (0,0,320,440)
wv.name = 'webview1'

class side_bar(ui.View):
	def did_load(self):
		self["sb"].alpha = 0
		
class iGitHub(ui.View):
	def did_load(self):
		self["mb"].action = show_menu_bar
		
gui = ui.load_view('igithub')

def getrepo(sender):
	usr = sender.superview["usr"].text
	rep = sender.superview["rep"].text
	url = 'https://codeload.github.com/{}/{}/zip/master'.format(usr, rep)
	filename, headers = urllib.urlretrieve(url)
	with zipfile.ZipFile(filename) as zip_file:
		zip_file.extractall()
		
def sb_clicked(sender):
	global gr_open, gh_open
	button = sender.items[sender.selected_row]['title']
	scroll = gui["scrollview1"]
	show_menu_bar(gui["view1"]["mb"])
	if button == 'Get Repository':
		gr_open=True
		for subview in (lbl1, usrt, lbl2, psdt, btn):
			scroll.add_subview(subview)
		scroll["getrepo"].action=getrepo
		if gh_open:
			gh_open = False
			scroll.remove_subview(scroll["webview1"])
	elif button == 'GitHub':
		gh_open=True
		scroll.add_subview(wv)
		wv.load_url('http://www.github.com')
		if gr_open:
			for subview_name in 'label1 usr label2 rep getrepo'.split():
				scroll.remove_subview(scroll[subview_name])
				
gui["view2"]["sb"].delegate.action=sb_clicked

gui.present("fullscreen", hide_title_bar=True)

