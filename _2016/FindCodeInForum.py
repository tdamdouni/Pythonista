#!python2

# coding: utf-8

# https://github.com/humberry/FindCodeInForum/blob/master/FindCodeInForum.py

# https://forum.omz-software.com/topic/2788/share-code-findcodeinforum

from __future__ import print_function
import dialogs, bs4, urllib2

field_url=[{'type':'url', 'key':'url', 'value':'', 'title':'URL:'}]
field_filter=[{'type':'switch', 'key':'python', 'value':False, 'title':'python'},
    {'type':'switch', 'key':'xml', 'value':False, 'title':'xml'},
    {'type':'switch', 'key':'json', 'value':False, 'title':'json'},
    {'type':'switch', 'key':'allcode', 'value':True, 'title':'all'}]
fields_file=[{'type':'switch', 'key':'savefile', 'value':True, 'title':'Save as file'},
    {'type':'text', 'key':'filename', 'value':'sourcecode.txt', 'title':'Filename:'}]
sections=[('',field_url),('Filter',field_filter),('File',fields_file)]
items = dialogs.form_dialog(title='FindCodeInForum', fields=None, sections=sections)
if items:
	url = items.get('url')
	cpython = items.get('python')
	cxml = items.get('xml')
	cjson = items.get('json')
	call = items.get('allcode')
	savefile = items.get('savefile')
	filename = items.get('filename')
	if savefile and filename == '':
		print('Please type in a valid filename!')
	else:
		c = []
		soup = bs4.BeautifulSoup(urllib2.urlopen(url).read())
		if cpython:
			allpython = soup.find_all('code','python')
			for code in allpython:
				c.append(['py',code.getText()])
		if cxml:
			allxml = soup.find_all('code','xml')
			for code in allxml:
				c.append(['xml',code.getText()])
		if cjson:
			alljson = soup.find_all('code','json')
			for code in alljson:
				c.append(['json',code.getText()])
		if call:
			alljson = soup.find_all('code')
			for code in alljson:
				c.append(['all',code.getText()])
		if c:
			cb = dialogs.edit_list_dialog('Codeblocks', c)
			if savefile:
				file = open(filename, 'a')          # append/create file
				for c in cb:
					file.write(c[1])
					file.write('# --------------------\n')    #seperator for different code blocks
				file.close()
				print('File ' + filename + ' is created.')
			else:
				for c in cb:
					print(c[1])
					print('# --------------------\n')    #seperator for different code blocks
		else:
			print('Sorry nothing found.')

