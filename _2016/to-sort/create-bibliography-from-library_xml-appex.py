# coding: utf-8

# http://pastebin.com/gmzw8ZyM

# 2016-03-12 v0.1a
# This script is supposed to be run as an extension from the share sheet and accepts text input
# For reference management and Bibliography creation you have to provide a well formed Library.xml
# For ToC creation you have to provide Markdown headers h2 (##) to h4 (####)
# USE AT YOUR OWN RISK – no support provided

from __future__ import print_function
import appex
import console
import clipboard
import xmltodict

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
		
	# Input from extension/share sheet
	txt = appex.get_text()
	
	if not txt:
		print('No text input found.')
		return
	else:
		txt = createToC(txt)
		txt = ref(txt)
		
		# Output to clipboard
		clipboard.set(txt)
		
def ref(txt):
	# Replace citekeys with full references and create Bibliography
	lib = open('Library.xml')
	dom = xmltodict.parse(lib)
	lib.close()
	rec = 0
	references = {}
	replaced = 0
	biblio = {}
	bibtxt = ''
	oldtxt = txt
	
	# Get reference data from Library.xml
	for entry in dom['xml']['entry']:
		citekey = dom['xml']['entry'][rec]['citekey']['@x']
		try:
			author = dom['xml']['entry'][rec]['author']['@x']
		except:
			author = ''
			#print 'Autor fehlt: '+citekey
		try:
			title = dom['xml']['entry'][rec]['title']['@x'].replace('üüUNDüü','&').replace('\'\'','"')
		except:
			title = ''
			#print 'Titel fehlt: '+citekey
		try:
			year = dom['xml']['entry'][rec]['year']['@x']
		except:
			year = ''
			#print 'Jahr fehlt: '+citekey
		try:
			place = bla['xml']['entry'][rec]['place']['@x']
		except:
			place = ''
			#print 'Ort fehlt: '+citekey
		tmpref = {citekey : author+': '+title+'. '+place+' '+year+'.'}
		references.update(tmpref)
		rec = rec+1
		
	# Replace citekeys
	for (k,v) in references.iteritems():
		txt = txt.replace(k,v)
		if k in oldtxt:
			tmpbib = {k : v}
			biblio.update(tmpbib)
		if txt != oldtxt:
			replaced = replaced+oldtxt.count(k)
			
	if replaced > 0:
		#console.hud_alert('Ersetzungen: '+str(replaced),'success')
		console.hud_alert('Replaced: '+str(replaced),'success')
		
		#       Bulid Bibliography
		for v in sorted(biblio.values()):
			bibtxt = bibtxt+'- '+v+'\n'
		#txt = txt+'\n----\n# Literatur\n'+bibtxt
		txt = txt+'\n----\n# Bibliography\n'+bibtxt
		
	else:
		#console.hud_alert('Keine Citekeys zum Ersetzen gefunden.','error')
		console.hud_alert('No citekeys found.','error')
		
	return txt
	
def createToC(txt):
	toctxt = ''
	cnt1 = 0
	cnt2 = 0
	cnt3 = 0
	toc = {}
	for line in txt.splitlines():
		if line.startswith('## '):
			cnt1 = cnt1+1
			cnt2 = 0
			tmptoc = {str(cnt1)+'.' : line[3:]}
			toc.update(tmptoc)
		if line.startswith('### '):
			cnt2 = cnt2+1
			cnt3 = 0
			tmptoc = {str(cnt1)+'.'+str(cnt2)+'.' : line[4:]}
			toc.update(tmptoc)
		if line.startswith('#### '):
			cnt3 = cnt3+1
			tmptoc = {str(cnt1)+'.'+str(cnt2)+'.'+str(cnt3)+'.' : line[5:]}
			toc.update(tmptoc)
	for (k,v) in sorted(toc.iteritems()):
		toctxt = toctxt+k+v+'\n'
		txt = txt.replace('## '+v,'## '+k+' '+v)
		txt = txt.replace('### '+v,'### '+k+' '+v)
		txt = txt.replace('#### '+v,'#### '+k+' '+v)
	toctxt = toctxt.replace('.','. ')
	#txt = '# Inhalt\n'+toctxt+'\n----\n'+txt
	txt = '# Table of Contents\n'+toctxt+'\n----\n'+txt
	return txt
	
if __name__ == '__main__':
	main()

