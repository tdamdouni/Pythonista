# coding: utf-8

# https://forum.omz-software.com/topic/2961/ui-webview-in-an-extension/3

# The HTML I'm using works everywhere, but not loaded through in an extension. That's my whole goal, I am trying to replace webbrowser.open("local file") for use in an extension. I haven't tried to load a local image using my HTML doc, I'll try that out.
# Here is an example of my HTML when I point it at "http://xkcd.com"

# Here is my full code (cleaned and formatted, but just as dysfunctional when used as an extension):

# coding: utf-8

from __future__ import print_function
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
		print('\n'.join(pics))
		
def main():
	if not appex.is_running_extension():
		print('\nRunning using test data...')
		url = 'http://xkcd.com'
	else:
		url = appex.get_url()
	if url:
		pick(url)
	else:
		print('No input URL found.')
		
if __name__ == '__main__':
	main()

