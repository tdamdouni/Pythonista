# coding: utf-8

# @Editorial Workflow

# https://gist.github.com/wcaleb/b6a8c97ccb0f11bd16ab

## For more information, see:
## http://www.docverter.com/api.html
## http://wcm1.web.rice.edu/pandoc-on-ios.html
## http://www.editorial-workflows.com/workflow/6394998534701056/p2vZ5Pj3570

import httplib
import mimetypes
import re
import StringIO
import editor
import clipboard
import os
import ui, workflow

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

## Custom UI action functions

# switch
def switch_action(sender):
	param = (sender.name, "true")
	if sender.value:
		fields.append(param)
	elif param in fields and not sender.value:
		fields.remove(param)

# switch
def set_strict(sender):
	global formats
	formats['from'] = formats['from'] + '_strict'

# tableview: markdown, html, latex
def set_to(sender):
	global formats
	selection = sender.items[sender.selected_row]
	formats['to'] = selection['title']

# tableview: markdown, html, latex
def set_from(sender):
	global formats
	selection = sender.items[sender.selected_row]
	formats['from'] = selection['title']

# button
def out_to_editor(sender):
	request = post_multipart("c.docverter.com", "/convert", formats.items() + fields, files)
	buffer = StringIO.StringIO(request)
	output = buffer.getvalue()
	editor.replace_text(0, 0, output)
	buffer.close()
	view.close()
	workflow.stop()

# button
def out_to_clipboard(sender):
	request = post_multipart("c.docverter.com", "/convert", formats.items() + fields, files)
	buffer = StringIO.StringIO(request)
	output = buffer.getvalue()
	clipboard.set(output)
	buffer.close()
	view.close()
	workflow.stop()
	
# Program Body

formats = {}
fields = []
files = [("input_files[]", "docverterin.txt", open("docverterin.txt", "r").read())]

text = editor.get_text()

fw = open("docverterin.txt", "w")
fw.write("Hello world!")
fw.close()
	
view = None
view = ui.load_view()
view.present('popover')