# coding: utf-8

# https://forum.omz-software.com/topic/2961/ui-webview-in-an-extension/4

import ui
def view(text):
	v = ui.View()
	wv = ui.WebView()
	v.add_subview(wv)
	wv.load_html(text)
	v.frame = (0,0,320,568)
	wv.frame = (0,0,320,568)
	v.present()
	
# --------------------

# coding: utf-8

import ui
import appex

text = appex.get_text()

if text:
	w = ui.WebView()
	w.scales_page_to_fit = False
	w.load_html(text)
	w.present()
# --------------------
<h1>header</h1>
<b>some bold text</b>
<img src= "https://lh4.ggpht.com/wKrDLLmmxjfRG2-E-k5L5BUuHWpCOe4lWRF7oVs1Gzdn5e5yvr8fj-ORTlBF43U47yI=w300"></img>
# --------------------
import ui
text="<img src='http://omz-software.com/pythonista/images/DeviceScreenshots.png'></img>"
def view(text):
	v = ui.View()
	wv = ui.WebView()
	v.add_subview(wv)
	wv.load_html(text)
	v.frame = (0,0,320,568)
	wv.frame = (0,0,320,568)
	v.present()
view(text)
# --------------------
<html>
<body bgcolor="#000000">
<img src="http://imgs.xkcd.com/static/terrible_small_logo.png" alt="http://imgs.xkcd.com/static/terrible_small_logo.png" ><br><br>
<img src="http://imgs.xkcd.com/comics/tire_swing.png" alt="http://imgs.xkcd.com/comics/tire_swing.png" ><br><br>
<img src="http://imgs.xkcd.com/store/te-pages-sb.png" alt="http://imgs.xkcd.com/store/te-pages-sb.png" ><br><br>
<img src="http://imgs.xkcd.com/s/a899e84.jpg" alt="http://imgs.xkcd.com/s/a899e84.jpg" >
</body>
</html>

# --------------------

# coding: utf-8

import appex

from urllib2 import urlopen
import os, console, requests, urlparse

def write_text(name, text, writ='w'):
	with open(name, writ) as o:
		o.write(text)
		
def img_page(file_list, link_list=None):
	if link_list is None: link_list = file_list
	links = zip(file_list, link_list)
	x = '<br><br>\n'.join(['<img src="{0}" alt="{1}" >'.format(a,b) for a,b in links])
	y = """
	<html>
	<body bgcolor="#000000">
	{0}
	</body>
	</html>
	""".format(x)
	return y
	
def view_doc(text):
	import ui
	w = ui.WebView()
	w.scales_page_to_fit = False
	w.load_html(text)
	w.present()
	
def open_file(file_path):
	import ui
	file_path = os.path.abspath(file_path)
	file_path = urlparse.urljoin('file://', os.path.abspath(file_path))
	#v = ui.View()
	#file_path = 'http://xkcd.com'
	wv = ui.WebView()
	#v.add_subview(wv)
	wv.load_url(file_path)
	#v.frame = (0,0,320,568)
	#wv.frame = (0,0,320,568)
	#v.present()
	wv.present()
	
def view_temp_index(file_url_list):
	temp_fn = '__temp.html'
	write_text(temp_fn, img_page(file_url_list))
	open_file(temp_fn)
	
def get_Pic_Links_Content(content,url=None):
	from bs4 import BeautifulSoup as bs
	if url is None:
		url = '' # 'http://'
	s = bs(content)
	p = s.findAll('img')
	pics = []
	for x in p:
		y = urlparse.urljoin(url, x['src'])
		if y not in pics:
			pics.append(y)
	return pics
	
def get_Pic_Links(url):
	r = requests.get(url)
	#print 'viewing pics from url:', r.url
	return get_Pic_Links_Content(r.content, url)
	
def pick(url):
	choice = console.alert('View:','Pick where to view source:','Make File','View Directly','Console')
	pics = get_Pic_Links(url)
	
	if choice == 1:
		view_temp_index(pics)
	elif choice == 2:
		view_doc(img_page(pics))
	else:
		print '\n'.join(pics)
		
def main():
	if not appex.is_running_extension():
		print '\nRunning using test data...'
		url = 'http://xkcd.com'
	else:
		url = appex.get_url()
	if url:
		pick(url)
	else:
		print 'No input URL found.'
		
if __name__ == '__main__':
	main()
	
# --------------------

