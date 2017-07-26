#! /usr/bin/env python2
# -*- coding: utf-8 -*-

## iMDtoPDF.py
## by W. Caleb McDaniel
## http://wcm1.web.rice.edu

## This is a wrapper script for sending documents to Docverter
## for conversion from markdown to PDF using Pandoc. Typically
## Docverter calls are made with cURL; this script uses httplib.
## It is intended for use with Pythonista on iOS, so output file
## is uploaded to Dropbox after document conversion.
## For more information, see: http://www.docverter.com/api.html

import clipboard
import datetime
import httplib
import mimetypes

## https://gist.github.com/omz/4034526
## http://omz-software.com/pythonista/forums/discussion/10/using-the-dropbox-module/p1
from dropboxloginv2 import get_client
dropbox_client = get_client()

## Helper functions for posting multipart/form-data request
## using standard libraries. Updated to reflect changes to
## httplib in Python 2.0.
## {{{ http://code.activestate.com/recipes/146306/ (r1)

def post_multipart(host, selector, fields, files):
	"""
	Post fields and files to an http host as multipart/form-data.
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files
	Return the server's response page.
	"""
	content_type, body = encode_multipart_formdata(fields, files)
	h = httplib.HTTPConnection(host)
	h.putrequest('POST', selector)
	h.putheader('content-type', content_type)
	h.putheader('content-length', str(len(body)))
	h.endheaders()
	h.send(body)
	response = h.getresponse()
	output = response.read()
	return output
	# return h.file.read()
	
def encode_multipart_formdata(fields, files):
	"""
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files
	Return (content_type, body) ready for httplib.HTTP instance
	"""
	BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
	CRLF = '\r\n'
	L = []
	for (key, value) in fields:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"' % key)
		L.append('')
		L.append(value)
	for (key, filename, value) in files:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
		L.append('Content-Type: %s' % get_content_type(filename))
		L.append('')
		L.append(value)
	L.append('--' + BOUNDARY + '--')
	L.append('')
	body = CRLF.join(L)
	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
	return content_type, body
	
def get_content_type(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
	
## end of http://code.activestate.com/recipes/146306/ }}}

## Now let's DO this. First put some markdown text on your clipboard.

## Put clipboard contents in a file to send to Docverter.
#input_text = clipboard.get()
#f = open("docverterin.txt", "w").write(input_text)

## support markdown documents with ASCII characters
input_text = clipboard.get()
input_text = input_text.encode('ascii', 'xmlcharrefreplace')
f = open("docverterin.txt", "w").write(input_text)

## Use CSS to style your output. I've included some sensible defaults.
css = """
body {margin: 4em; }
p {line-height: 1.2em; text-align: justify;}
h1, h2, h3, h4 {font-weight: normal;}
sup {line-height: 0;}
hr {border: 1px #eee solid; margin-top: 2em; margin-botom: 2em; width: 70%;}
pre {white-space: pre-wrap; word-wrap: break-word;}
"""
# Use CSS3 Paged Media Module to number pages of PDF, set margins.
page_info = "@page {margin: 1in; @bottom-center{content: counter(page)}}"
c = open("docverter.css", "w").write(css + page_info)

## Set Docverter options and define fields using lists.
## Other options available at http://www.docverter.com/api.html#toc_2
fields = [("from", "markdown"), ("to", "pdf"), ("css", "docverter.css")]
files = [("input_files[]", "docverterin.txt", open("docverterin.txt", "r").read()), ("other_files[]", "docverter.css", open("docverter.css","r").read())]

## Post to Docverter using post_multipart()
output = post_multipart("c.docverter.com", "/convert", fields, files)

## Write output to a PDF file, appending timestamp to filename.
today = datetime.datetime.now()
outfile = 'output-' + today.strftime('%Y%m%d-%H%M%S') + '.pdf'
o = open(outfile, "w").write(output)

## Upload file to Dropbox, appending timestamp to filename
o = open(outfile)
upload = dropbox_client.put_file(outfile, o)

