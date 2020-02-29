# coding: utf-8

# https://github.com/humberry/Hyperlink2PDF/tree/master 

# Hyperlink2PDF

# Insert URL and get a PDF with all Hyperlinks
# Delete or re-sort Hyperlinks before they are saved.
# You need the reportlab module!

from __future__ import print_function
from bs4 import BeautifulSoup
import urllib2, dialogs
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

items = dialogs.form_dialog(title='Hyperlink2PDF', fields=[{'type':'url','key':'url','value':'http://','title':'URL:'},{'type':'text','key':'filename','value':'urls.pdf','title':'Filename:'},{'type':'switch','key':'format','value':True,'title':'A4 (Letter)'},{'type':'switch','key':'imagelink','value':True,'title':'Image Hyperlinks'},{'type':'switch','key':'qmlink','value':True,'title':'??? Hyperlinks'}], sections=None)
if items != None:
	url = items.get('url')
	filename = items.get('filename')
	format = items.get('format')	#True = A4 / False = letter
	imagelink = items.get('imagelink')
	qmlink = items.get('qmlink')
	if url == 'http://' or url == '' or filename == '':
		print('Please type in a valid website/filename!')
	else:
		urlcontent = urllib2.urlopen(url).read()
		start = url.find('://') + 3
		domain = ''
		end = url.find('/', start)
		if end == -1:
			domain = url
		else:
			domain = url[:end]
		soup = BeautifulSoup(urlcontent)
		
		links = soup.find_all('a')
		hl = []
		s = ''
		for link in links:
			text = link.get_text(" | ", strip=True)
			hlurl = link.get('href')
			if len(text) == 0:
				if link.find('img') != None:
					if imagelink:
						text = '[image]'
					else:
						continue
				else:
					if qmlink:
						text = '[???]'
					else:
						continue
			if '#' in hlurl and not '.' in hlurl:	#only shortcuts to other websites
				continue
			if hlurl[0] == '/':
				hlurl = domain + hlurl
			hl.append([text, hlurl])
		
		l = dialogs.edit_list_dialog('Hyperlinks',hl)
		
		style = getSampleStyleSheet()
		items = []
		for i in l:
			items.append(Paragraph('<link href="' + i[1] + '" color="blue">' + i[0] + '</link>', style['Heading3']))
		if format:
			pdf = SimpleDocTemplate(filename, pagesize=A4)
		else:
			pdf = SimpleDocTemplate(filename, pagesize=letter)
		pdf.build(items)
		print('PDF is created.')
